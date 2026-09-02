import apiClient from './api.js'

export const jobService = {
  // Create new job
  async createJob(jobData) {
    const response = await apiClient.post('/api/jobs', jobData)
    return response.data
  },

  // Get all jobs
  async getJobs() {
    const response = await apiClient.get('/api/jobs')
    return response.data
  },

  // Get single job
  async getJob(jobId) {
    const response = await apiClient.get(`/api/jobs/${jobId}`)
    return response.data
  }
}

export default jobService
