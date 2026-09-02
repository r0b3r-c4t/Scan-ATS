import React from 'react'
import './ScoreBreakdown.css'

export const ScoreBreakdown = ({ breakdown = {} }) => {
  const items = Object.entries(breakdown).filter(([_, value]) => value !== undefined)

  if (items.length === 0) {
    return null
  }

  return (
    <div className="score-breakdown">
      <h3>Score Breakdown</h3>
      <div className="breakdown-items">
        {items.map(([label, score]) => (
          <div key={label} className="breakdown-item">
            <div className="breakdown-label">{label}</div>
            <div className="breakdown-bar">
              <div
                className="breakdown-progress"
                style={{ width: `${score}%` }}
              />
            </div>
            <div className="breakdown-value">{score}%</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ScoreBreakdown
