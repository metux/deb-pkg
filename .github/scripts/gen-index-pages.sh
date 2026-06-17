#!/bin/bash
ROOT=.aptrepo
BASE_URL=https://metux.github.io/deb-pkg

[ -d "$ROOT" ] || exit 0

# Root overview page
{
  cat <<EOF
<html><body>
<h1>deb-pkg apt repos</h1>
<p>Automatically built apt repositories. See each pool for sources.list instructions.</p>
<ul>
EOF
  for pool in "$ROOT"/*/; do
    [ -d "$pool" ] || continue
    pname=$(basename "$pool")
    echo "<li><a href=\"$pname/\">$pname</a>"
    pkgcount=$(find "$pool" -name "*.deb" 2>/dev/null | wc -l)
    echo " ($pkgcount packages)</li>"
  done
  echo '</ul>'
  echo '</body></html>'
} > "$ROOT/index.html"

# Per-pool pages
for pool in "$ROOT"/*/; do
    [ -d "$pool" ] || continue
    pool="${pool%/}"
    pname=$(basename "$pool")

    # Find apt repo subdirectories (e.g. devuan/excalibur)
    for repodir in "$pool"/*/; do
        [ -d "$repodir" ] || continue
        repodir="${repodir%/}"
        rname=$(basename "$repodir")

    # Find suite directories (distro)
    for distdir in "$repodir"/*/; do
      [ -d "$distdir" ] || continue
      dname=$(basename "$distdir")

      # Check if it's an apt repo (has dists/)
      if [ -d "${distdir}dists" ]; then
        {
          cat <<EOF
<html><body>
<h1>Pool: $pname</h1>
<h2>apt sources.list</h2>
<pre>deb $BASE_URL/$pname/$rname/$dname $dname main</pre>
<h2>Key</h2>
EOF
          keyfile="${distdir}apt-repo.pub"
          if [ -f "$keyfile" ]; then
            relkey="${keyfile#$pool/}"
            keysha=$(sha256sum "$keyfile" 2>/dev/null | cut -d' ' -f1)
            cat <<EOF
<p><a href="$relkey">$relkey</a></p>
<pre>SHA256: $keysha</pre>
EOF
          else
            echo '<p>No signing key published.</p>'
          fi

          echo '<h2>Release files</h2><ul>'
          release="${distdir}dists/$dname/Release"
          if [ -f "$release" ]; then
            rel="${release#$pool/}"
            echo "<li><a href=\"$rel\">Release</a></li>"
          fi
          releasegpg="${distdir}dists/$dname/Release.gpg"
          if [ -f "$releasegpg" ]; then
            rel="${releasegpg#$pool/}"
            echo "<li><a href=\"$rel\">Release.gpg</a></li>"
          fi
          echo '</ul>'

          echo '<h2>Packages</h2><table border="1"><tr><th>Package</th><th>Size</th><th>SHA256</th></tr>'
          find "${distdir}pool" -name "*.deb" 2>/dev/null | sort | while read f; do
            rel="${f#$pool/}"
            size=$(stat -c%s "$f" 2>/dev/null || echo 0)
            sha=$(sha256sum "$f" 2>/dev/null | cut -d' ' -f1)
            echo "<tr><td><a href=\"$rel\">$(basename $f)</a></td><td>$size</td><td><tt>$sha</tt></td></tr>"
          done
          echo '</table></body></html>'
        } > "$pool/index.html"
      fi
    done
  done
done
