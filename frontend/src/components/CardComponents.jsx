import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ScoreCard } from './ScoreRing'
import "./CardComponents.css"

export const CandidateCard = ({ candidate, onClick = null }) => {
  const navigate = useNavigate()
  const score = candidate.candidate_score?.score || candidate.candidate_score || 0
  const classification = candidate.candidate_score?.classification || 'Unknown'

  const handleClick = () => {
    if (onClick) {
      onClick(candidate)
    } else {
      navigate(`/candidates/${candidate._id || candidate.id}`)
    }
  }

  return (
    <div className="candidate-card" onClick={handleClick}>
      <div className="candidate-card-header">
        <div className="candidate-info">
          <h3>{candidate.name}</h3>
          <p>{candidate.email}</p>
        </div>
        <div className="candidate-score-badge">
          <div className="score-number">{Math.round(score)}</div>
          <div className="score-badge-text">{classification}</div>
        </div>
      </div>

      {candidate.technical_skills && (
        <div className="candidate-skills">
          <div className="skills-label">Skills</div>
          <div className="skills-preview">
            {(typeof candidate.technical_skills === 'string'
              ? candidate.technical_skills.split('·').slice(0, 3)
              : Array.isArray(candidate.technical_skills)
              ? candidate.technical_skills.slice(0, 3)
              : []
            ).map((skill, idx) => (
              <span key={idx} className="skill-tag">
                {typeof skill === 'string' ? skill.trim() : skill}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="candidate-actions">
        <button className="action-link">View Profile →</button>
      </div>
    </div>
  )
}

export const JobCard = ({ job, onClick = null }) => {
  const navigate = useNavigate()

  const handleClick = () => {
    if (onClick) {
      onClick(job)
    } else {
      navigate(`/jobs/${job._id || job.id}`)
    }
  }

  return (
    <div className="job-card" onClick={handleClick}>
      <div className="job-card-header">
        <h3>{job.title}</h3>
        <span className="job-badge">{job.required_skills?.length || 0} skills</span>
      </div>

      <p className="job-description">{job.description || 'No description'}</p>

      {job.required_skills && (
        <div className="job-skills">
          <div className="skills-label">Required Skills</div>
          <div className="skills-preview">
            {job.required_skills.slice(0, 3).map((skill, idx) => (
              <span key={idx} className="skill-tag">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="job-actions">
        <button className="action-link">View Job →</button>
      </div>
    </div>
  )
}

export default { CandidateCard, JobCard }
