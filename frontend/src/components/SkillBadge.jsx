import React from 'react'
import './SkillBadge.css'

export const SkillBadge = ({ skills = [], variant = 'default', matched = null }) => {
  if (!skills || skills.length === 0) {
    return <p className="text-muted">No skills</p>
  }

  const skillArray = typeof skills === 'string' 
    ? skills.split('·').map(s => s.trim())
    : Array.isArray(skills) 
    ? skills 
    : []

  return (
    <div className="skill-badges">
      {skillArray.map((skill, index) => (
        <span
          key={index}
          className={`skill-badge skill-badge-${variant} ${matched !== null && (matched[index] ? 'matched' : 'unmatched')}`}
        >
          {matched !== null && (matched[index] ? '✓ ' : '✕ ')}
          {skill}
        </span>
      ))}
    </div>
  )
}

export default SkillBadge
