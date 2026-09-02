import apiClient from './api.js'

export const candidateService = {
  // Upload resume
  async uploadResume(file) {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post('/api/candidates/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Get all candidates
  async getCandidates() {
    const response = await apiClient.get('/api/candidates')
    return response.data
  },

  // Get single candidate
  async getCandidate(candidateId) {
    const response = await apiClient.get(`/api/candidates/${candidateId}`)
    return response.data
  },

  // Get candidate score
  async getCandidateScore(candidateId) {
    const response = await apiClient.get(`/api/candidates/${candidateId}/score`)
    return response.data
  },

  // Download/view candidate resume
  async downloadResume(candidateId) {
    const response = await apiClient.get(`/api/candidates/${candidateId}/resume`, {
      responseType: 'blob'
    })
    return response.data
  },

  // Get resume URL for viewing (opens in new tab)
  getResumeUrl(candidateId) {
    return `${apiClient.defaults.baseURL}/api/candidates/${candidateId}/resume`
  }
}

export default candidateService
