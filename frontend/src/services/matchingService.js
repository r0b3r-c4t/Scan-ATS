import apiClient from './api.js'

export const matchingService = {
  // Get match between candidate and job
  async getMatch(jobId, candidateId) {
    const response = await apiClient.get(
      `/api/jobs/${jobId}/candidates/${candidateId}/match`
    )
    return response.data
  },

  // Get all matches for a job
  async getJobMatches(jobId) {
    const response = await apiClient.get(`/api/jobs/${jobId}/matches`)
    return response.data
  }
}

export default matchingService
