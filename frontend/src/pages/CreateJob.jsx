import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import jobService from '../services/jobService'
import { ErrorState } from '../components/StateComponents'
import './CreateJob.css'

const CreateJob = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    required_skills: [],
    preferred_skills: [],
    minimum_experience: '',
    education_requirements: '',
    required_certifications: []
  })
  const [currentSkill, setCurrentSkill] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleAddSkill = (type) => {
    if (currentSkill.trim()) {
      setFormData(prev => ({
        ...prev,
        [type]: [...prev[type], currentSkill.trim()]
      }))
      setCurrentSkill('')
    }
  }

  const handleRemoveSkill = (type, index) => {
    setFormData(prev => ({
      ...prev,
      [type]: prev[type].filter((_, i) => i !== index)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.title.trim()) {
      setError('Job title is required')
      return
    }

    try {
      setLoading(true)
      setError(null)
      
      const jobData = {
        ...formData,
        required_skills: formData.required_skills.filter(s => s),
        preferred_skills: formData.preferred_skills.filter(s => s),
        required_certifications: formData.required_certifications.filter(c => c)
      }

      const response = await jobService.createJob(jobData)
      navigate(`/jobs/${response._id || response.id}`)
    } catch (err) {
      console.error('Error creating job:', err)
      setError(err.response?.data?.detail || 'Failed to create job')
      setLoading(false)
    }
  }

  if (error && !formData.title) {
    return <ErrorState message={error} onRetry={() => setError(null)} />
  }

  return (
    <div className="create-job-page">
      <div className="form-container">
        <h1>Create New Job</h1>

        {error && (
          <div className="error-banner">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="job-form">
          <div className="form-group">
            <label htmlFor="title">Job Title *</label>
            <input
              id="title"
              type="text"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              placeholder="e.g., Backend Developer Junior"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              placeholder="Job description..."
            />
          </div>

          {/* Required Skills */}
          <div className="form-group">
            <label>Required Skills</label>
            <div className="skills-input">
              <input
                type="text"
                value={currentSkill}
                onChange={(e) => setCurrentSkill(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    handleAddSkill('required_skills')
                  }
                }}
                placeholder="Add skill..."
              />
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => handleAddSkill('required_skills')}
              >
                Add
              </button>
            </div>
            <div className="skills-list">
              {formData.required_skills.map((skill, idx) => (
                <div key={idx} className="skill-item">
                  <span>{skill}</span>
                  <button
                    type="button"
                    className="remove-btn"
                    onClick={() => handleRemoveSkill('required_skills', idx)}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Preferred Skills */}
          <div className="form-group">
            <label>Preferred Skills</label>
            <div className="skills-input">
              <input
                type="text"
                value={currentSkill}
                onChange={(e) => setCurrentSkill(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    handleAddSkill('preferred_skills')
                  }
                }}
                placeholder="Add skill..."
              />
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => handleAddSkill('preferred_skills')}
              >
                Add
              </button>
            </div>
            <div className="skills-list">
              {formData.preferred_skills.map((skill, idx) => (
                <div key={idx} className="skill-item">
                  <span>{skill}</span>
                  <button
                    type="button"
                    className="remove-btn"
                    onClick={() => handleRemoveSkill('preferred_skills', idx)}
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="experience">Minimum Experience</label>
            <input
              id="experience"
              type="text"
              name="minimum_experience"
              value={formData.minimum_experience}
              onChange={handleInputChange}
              placeholder="e.g., 2 years"
            />
          </div>

          <div className="form-group">
            <label htmlFor="education">Education Requirements</label>
            <input
              id="education"
              type="text"
              name="education_requirements"
              value={formData.education_requirements}
              onChange={handleInputChange}
              placeholder="e.g., Bachelor's in Computer Science"
            />
          </div>

          <div className="form-actions">
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Job'}
            </button>
            <button 
              type="button" 
              className="btn btn-secondary"
              onClick={() => navigate('/jobs')}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateJob
