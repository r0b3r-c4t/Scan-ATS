import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import jobService from '../services/jobService'
import matchingService from '../services/matchingService'
import { SkillBadge } from '../components/SkillBadge'
import { LoadingState, ErrorState } from '../components/StateComponents'
import './JobDetail.css'

const JobDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [job, setJob] = useState(null)
  const [matches, setMatches] = useState([])
  const [selectedMatch, setSelectedMatch] = useState(null)
  const [matchDetail, setMatchDetail] = useState(null)
  const [loading, setLoading] = useState(true)
  const [loadingMatches, setLoadingMatches] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadJobData()
  }, [id])

  const loadJobData = async () => {
    try {
      setLoading(true)
      setError(null)

      const jobData = await jobService.getJob(id)
      setJob(jobData)

      setLoadingMatches(true)
      const matchesData = await matchingService.getJobMatches(id)
      setMatches(matchesData)
    } catch (err) {
      console.error('Error loading job:', err)
      setError('Failed to load job')
    } finally {
      setLoading(false)
      setLoadingMatches(false)
    }
  }

  const handleSelectMatch = async (candidateId) => {
    try {
      setLoadingMatches(true)
      const detail = await matchingService.getMatch(id, candidateId)
      setSelectedMatch(candidateId)
      setMatchDetail(detail)
    } catch (err) {
      console.error('Error loading match detail:', err)
      setError('Failed to load match details')
    } finally {
      setLoadingMatches(false)
    }
  }

  if (error && loading) {
    return <ErrorState message={error} onRetry={loadJobData} />
  }

  if (loading) {
    return <LoadingState message="Loading job..." />
  }

  if (!job) {
    return <ErrorState message="Job not found" />
  }

  return (
    <div className="job-detail">
      <button className="btn-back" onClick={() => navigate('/jobs')}>
        ← Back to Jobs
      </button>

      {/* Job Header */}
      <div className="job-header">
        <div>
          <h1>{job.title}</h1>
          {job.description && (
            <p className="job-description">{job.description}</p>
          )}
        </div>
      </div>

      {/* Job Details */}
      <div className="job-info-grid">
        {job.required_skills && (
          <div className="info-section">
            <h3>Required Skills</h3>
            <SkillBadge skills={job.required_skills} variant="primary" />
          </div>
        )}

        {job.preferred_skills && (
          <div className="info-section">
            <h3>Preferred Skills</h3>
            <SkillBadge skills={job.preferred_skills} />
          </div>
        )}

        {job.minimum_experience && (
          <div className="info-section">
            <h3>Minimum Experience</h3>
            <p>{job.minimum_experience}</p>
          </div>
        )}

        {job.education_requirements && (
          <div className="info-section">
            <h3>Education</h3>
            <p>{job.education_requirements}</p>
          </div>
        )}
      </div>

      {/* Candidate Matches */}
      <div className="matches-section">
        <h2>Candidate Matches</h2>

        {loadingMatches ? (
          <LoadingState message="Loading matches..." />
        ) : matches.length > 0 ? (
          <div className="matches-container">
            <div className="matches-list">
              {matches.map(match => (
                <div 
                  key={match.candidate_id}
                  className={`match-item ${selectedMatch === match.candidate_id ? 'active' : ''}`}
                  onClick={() => handleSelectMatch(match.candidate_id)}
                >
                  <div className="match-info">
                    <h3>{match.candidate_name}</h3>
                    <p>{match.classification}</p>
                  </div>
                  <div className="match-score">
                    <span className="percentage">{Math.round(match.match_percentage)}%</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Match Detail */}
            {matchDetail && (
              <div className="match-detail-panel">
                <h3>{matchDetail.candidate_id}</h3>
                
                <div className="match-score-display">
                  <div className="score-ring">
                    <div className="score-value">{Math.round(matchDetail.match_percentage)}</div>
                    <div className="score-max">/ 100</div>
                  </div>
                  <p className="classification">{matchDetail.classification}</p>
                </div>

                {matchDetail.scores && (
                  <div className="breakdown">
                    <h4>Score Breakdown</h4>
                    {Object.entries(matchDetail.scores).map(([label, score]) => (
                      <div key={label} className="breakdown-item">
                        <span>{label}</span>
                        <span>{score}%</span>
                      </div>
                    ))}
                  </div>
                )}

                {matchDetail.explanation && (
                  <div className="explanation">
                    <h4>Explanation</h4>
                    <p>{matchDetail.explanation}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        ) : (
          <p className="no-matches">No candidates available for matching</p>
        )}
      </div>
    </div>
  )
}

export default JobDetail
