import React from 'react'
import { getScoreColor, getClassificationLabel } from '../utils/scoreUtils'
import './ScoreRing.css'

export const ScoreRing = ({ score, size = 'md', type = 'candidate' }) => {
  const radius = size === 'lg' ? 60 : size === 'md' ? 50 : 35
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference
  const color = getScoreColor(score)

  return (
    <div className={`score-ring score-ring-${size}`}>
      <svg width={radius * 2 + 20} height={radius * 2 + 20}>
        <circle
          cx={radius + 10}
          cy={radius + 10}
          r={radius}
          className="score-ring-bg"
        />
        <circle
          cx={radius + 10}
          cy={radius + 10}
          r={radius}
          className="score-ring-progress"
          style={{
            strokeDasharray: circumference,
            strokeDashoffset: offset,
            stroke: color
          }}
        />
      </svg>
      <div className="score-ring-content">
        <div className="score-ring-value">{Math.round(score)}</div>
        <div className="score-ring-max">/ 100</div>
      </div>
    </div>
  )
}

export const ScoreCard = ({ score, type = 'candidate', showDetails = false }) => {
  const classification = getClassificationLabel(type, score)
  const icon = type === 'candidate' ? '⭐' : '🎯'

  return (
    <div className="score-card">
      <div className="score-card-header">
        <span className="score-card-icon">{icon}</span>
        <h3>{type === 'candidate' ? 'Candidate Score' : 'Match Score'}</h3>
      </div>
      <div className="score-card-body">
        <ScoreRing score={score} size="md" type={type} />
        <p className="score-card-classification">{classification}</p>
      </div>
    </div>
  )
}

export default ScoreRing
