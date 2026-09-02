export const getScoreClassification = (score) => {
  if (score >= 90) return 'Excellent'
  if (score >= 75) return 'Strong'
  if (score >= 60) return 'Moderate'
  if (score >= 40) return 'Weak'
  return 'Poor'
}

export const getScoreColor = (score) => {
  const classification = getScoreClassification(score)
  switch (classification) {
    case 'Excellent':
      return '#1B5E3B'
    case 'Strong':
      return '#2d7a4f'
    case 'Moderate':
      return '#f59e0b'
    case 'Weak':
      return '#ef4444'
    case 'Poor':
      return '#dc2626'
    default:
      return '#6b7280'
  }
}

export const getClassificationLabel = (type, score) => {
  if (type === 'candidate') {
    if (score >= 90) return 'Excellent Candidate'
    if (score >= 75) return 'Strong Candidate'
    if (score >= 60) return 'Moderate Candidate'
    if (score >= 40) return 'Weak Candidate'
    return 'Poor Candidate'
  } else if (type === 'match') {
    if (score >= 90) return 'Excellent Match'
    if (score >= 75) return 'Strong Match'
    if (score >= 60) return 'Moderate Match'
    if (score >= 40) return 'Weak Match'
    return 'Poor Match'
  }
  return 'Unknown'
}
