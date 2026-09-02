import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import candidateService from '../services/candidateService'
import { ScoreCard } from '../components/ScoreRing'
import { ScoreBreakdown } from '../components/ScoreBreakdown'
import { SkillBadge } from '../components/SkillBadge'
import { LoadingState, ErrorState } from '../components/StateComponents'
import './CandidateDetail.css'

const CandidateDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [candidate, setCandidate] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadCandidate()
  }, [id])

  const loadCandidate = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await candidateService.getCandidate(id)
      setCandidate(data)
    } catch (err) {
      console.error('Error loading candidate:', err)
      setError('Failed to load candidate')
    } finally {
      setLoading(false)
    }
  }

  if (error) {
    return <ErrorState message={error} onRetry={loadCandidate} />
  }

  if (loading) {
    return <LoadingState message="Loading candidate..." />
  }

  if (!candidate) {
    return <ErrorState message="Candidate not found" />
  }

  const score = candidate.candidate_score?.score || candidate.candidate_score || 0
  const evaluation = candidate.candidate_score || {}

  const handleViewResume = () => {
    if (candidate.resume?.file_id) {
      const resumeUrl = candidateService.getResumeUrl(id)
      window.open(resumeUrl, '_blank')
    }
  }

  return (
    <div className="candidate-detail">
      <button className="btn-back" onClick={() => navigate('/candidates')}>
        ← Back to Candidates
      </button>

      {/* Header */}
      <div className="candidate-header">
        <div className="candidate-info">
          <div className="header-top">
            <h1>{candidate.name || 'Unknown'}</h1>
            {candidate.resume?.file_id && (
              <button className="btn-view-resume" onClick={handleViewResume}>
                📄 View Resume
              </button>
            )}
          </div>
          <div className="candidate-meta">
            <span>{candidate.email || 'No email'}</span>
            {candidate.phone && <span>•</span>}
            {candidate.phone && <span>{candidate.phone}</span>}
            {candidate.location && <span>•</span>}
            {candidate.location && <span>{candidate.location}</span>}
          </div>
        </div>

        <div className="candidate-score-section">
          <ScoreCard score={score} type="candidate" />
        </div>
      </div>

      {/* Evaluation Breakdown */}
      {evaluation.scores && (
        <div className="candidate-section">
          <ScoreBreakdown breakdown={evaluation.scores} />
        </div>
      )}

      {/* Technical Skills */}
      {candidate.technical_skills && (
        <div className="candidate-section">
          <h2>Technical Skills</h2>
          <SkillBadge skills={candidate.technical_skills} variant="primary" />
        </div>
      )}

      {/* Experience */}
      {candidate.experience && candidate.experience.length > 0 && (
        <div className="candidate-section">
          <h2>Experience</h2>
          <div className="experience-list">
            {candidate.experience.map((exp, idx) => (
              <div key={idx} className="experience-item">
                <h3>{exp.title || 'Position'}</h3>
                <p className="company">{exp.company || 'Company'}</p>
                <p className="period">
                  {exp.start_date} - {exp.end_date || 'Present'}
                </p>
                {exp.description && <p>{exp.description}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Education */}
      {candidate.education && candidate.education.length > 0 && (
        <div className="candidate-section">
          <h2>Education</h2>
          <div className="education-list">
            {candidate.education.map((edu, idx) => {
              const isTextEntry = typeof edu === 'string'
              const title = isTextEntry
                ? edu
                : edu.degree || edu.name || edu.title || edu.program || 'Education'
              const institution = isTextEntry
                ? null
                : edu.school || edu.institution || edu.university || edu.organization
              const dates = isTextEntry
                ? null
                : edu.graduation_year || edu.dates || edu.date || edu.period

              return (
                <div key={idx} className="education-item">
                  <h3>{title}</h3>
                  {institution && <p className="school">{institution}</p>}
                  {dates && <p className="year">{dates}</p>}
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Certifications */}
      {candidate.certifications && candidate.certifications.length > 0 && (
        <div className="candidate-section">
          <h2>Certifications</h2>
          <div className="certifications-list">
            {candidate.certifications.map((cert, idx) => (
              <div key={idx} className="certification-item">
                <h3>{cert.name || 'Certification'}</h3>
                {cert.issuer && <p>{cert.issuer}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Projects */}
      {candidate.projects && candidate.projects.length > 0 && (
        <div className="candidate-section">
          <h2>Projects</h2>
          <div className="projects-list">
            {candidate.projects.map((project, idx) => (
              <div key={idx} className="project-item">
                <h3>{project.name || 'Project'}</h3>
                {project.description && <p>{project.description}</p>}
                {project.technologies && (
                  <SkillBadge skills={project.technologies} />
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary */}
      {candidate.summary && (
        <div className="candidate-section">
          <h2>Summary</h2>
          <div className="summary-text">
            {candidate.summary}
          </div>
        </div>
      )}
    </div>
  )
}

export default CandidateDetail
