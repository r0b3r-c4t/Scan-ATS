import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import jobService from '../services/jobService'
import matchingService from '../services/matchingService'
import { LoadingState, ErrorState, EmptyState } from '../components/StateComponents'
import './Matches.css'

const Matches = () => {
  const navigate = useNavigate()
  const [jobs, setJobs] = useState([])
  const [selectedJobId, setSelectedJobId] = useState(null)
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadingMatches, setLoadingMatches] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadJobs()
  }, [])

  useEffect(() => {
    if (selectedJobId) {
      loadMatches(selectedJobId)
    }
  }, [selectedJobId])

  const loadJobs = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await jobService.getJobs()
      setJobs(data)
      if (data.length > 0) {
        setSelectedJobId(data[0]._id || data[0].id)
      }
    } catch (err) {
      console.error('Error loading jobs:', err)
      setError('Failed to load jobs')
    } finally {
      setLoading(false)
    }
  }

  const loadMatches = async (jobId) => {
    try {
      setLoadingMatches(true)
      setError(null)
      const data = await matchingService.getJobMatches(jobId)
      setMatches(data)
    } catch (err) {
      console.error('Error loading matches:', err)
      setError('Failed to load matches')
    } finally {
      setLoadingMatches(false)
    }
  }

  if (error && loading) {
    return <ErrorState message={error} onRetry={loadJobs} />
  }

  if (loading) {
    return <LoadingState message="Loading matches..." />
  }

  return (
    <div className="matches-page">
      <div className="page-header">
        <div>
          <h1>Candidate Matches</h1>
          <p>Match candidates against job positions</p>
        </div>
      </div>

      {jobs.length === 0 ? (
        <EmptyState 
          message="No jobs available. Create a job first to see matches."
          icon="💼"
          actionLabel="Create Job"
          onAction={() => navigate('/jobs/new')}
        />
      ) : (
        <div className="matches-container">
          {/* Job Selector */}
          <div className="job-selector">
            <h3>Select Job</h3>
            <div className="job-list">
              {jobs.map(job => (
                <button
                  key={job._id || job.id}
                  className={`job-option ${selectedJobId === (job._id || job.id) ? 'active' : ''}`}
                  onClick={() => setSelectedJobId(job._id || job.id)}
                >
                  <span className="job-title">{job.title}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Matches Display */}
          <div className="matches-display">
            {loadingMatches ? (
              <LoadingState message="Loading matches..." />
            ) : matches.length > 0 ? (
              <div className="matches-table-container">
                <table className="matches-table">
                  <thead>
                    <tr>
                      <th>Candidate</th>
                      <th>Match Score</th>
                      <th>Classification</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {matches.map(match => (
                      <tr key={match.candidate_id}>
                        <td className="candidate-cell">
                          {match.candidate_name}
                        </td>
                        <td className="score-cell">
                          <span className="score-badge">
                            {Math.round(match.match_percentage)}%
                          </span>
                        </td>
                        <td className="classification-cell">
                          <span className={`classification ${getClassificationClass(match.classification)}`}>
                            {match.classification}
                          </span>
                        </td>
                        <td className="action-cell">
                          <button
                            className="btn btn-secondary btn-small"
                            onClick={() => navigate(`/jobs/${selectedJobId}`)}
                          >
                            View
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <EmptyState message="No candidates matched for this job" />
            )}
          </div>
        </div>
      )}
    </div>
  )
}

const getClassificationClass = (classification) => {
  if (!classification) return ''
  const lower = classification.toLowerCase()
  if (lower.includes('excellent')) return 'excellent'
  if (lower.includes('strong')) return 'strong'
  if (lower.includes('moderate')) return 'moderate'
  if (lower.includes('weak')) return 'weak'
  return 'poor'
}

export default Matches
