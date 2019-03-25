// this is the seeder job

def config = 'cf/default.yaml'

node {
    stage('cloning') {
        checkout scm
    }

    stage('info') {
        println("debkins_git_url=${debkins_git_url}")
        println("debkins_git_branch=${debkins_git_branch}")
        println("./debkins.jobgen \"${config}\" \"${debkins_git_url}\" \"${debkins_git_branch}\"")
    }

    stage('config') {
        sh('./debkins.jobgen '+config+' > seed.groovy')
    }

    stage('seeding') {
        jobDsl failOnMissingPlugin: true,
               lookupStrategy: 'SEED_JOB',
               removedConfigFilesAction: 'DELETE',
               removedJobAction: 'DELETE',
               removedViewAction: 'DELETE',
               targets: 'seed.groovy'
    }
}
