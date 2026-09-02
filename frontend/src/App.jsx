import React, { useState, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import CandidateList from './pages/CandidateList'
import CandidateDetail from './pages/CandidateDetail'
import UploadResume from './pages/UploadResume'
import JobList from './pages/JobList'
import CreateJob from './pages/CreateJob'
import JobDetail from './pages/JobDetail'
import Matches from './pages/Matches'
import Settings from './pages/Settings'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        
        <Route path="/candidates" element={<CandidateList />} />
        <Route path="/candidates/upload" element={<UploadResume />} />
        <Route path="/candidates/:id" element={<CandidateDetail />} />

        <Route path="/jobs" element={<JobList />} />
        <Route path="/jobs/new" element={<CreateJob />} />
        <Route path="/jobs/:id" element={<JobDetail />} />

        <Route path="/matches" element={<Matches />} />
        
        <Route path="/settings" element={<Settings />} />
        
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Layout>
  )
}

export default App
