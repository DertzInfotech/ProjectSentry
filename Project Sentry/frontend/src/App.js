import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Components
import Navigation from './components/Common/Navigation';
import Header from './components/Common/Header';
import Dashboard from './components/Dashboard/Dashboard';
import FileUpload from './components/Upload/FileUpload';
import IssuesList from './components/Issues/IssuesList';
import ModelViewer from './components/Viewer/ModelViewer';
import Loading from './components/Common/Loading';

// Services
import { apiService } from './services/api';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedProject, setSelectedProject] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    // Check if mobile
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);

    // Load initial data
    loadProjects();

    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);

      // Try to load from API, fall back to mock data
      try {
        const projectsData = await apiService.getProjects();
        setProjects(projectsData);

        // Select first project if available
        if (projectsData.length > 0 && !selectedProject) {
          setSelectedProject(projectsData[0]);
        }
      } catch (apiError) {
        console.log('API not available, using sample data for demo');
        // Use sample data for demo
        const sampleProjects = [
          {
            id: 'sample-1',
            name: 'Office Building Phase 2',
            filename: 'office_building_v2.ifc',
            file_size: '125.6 MB',
            upload_date: new Date().toISOString(),
            health_score: 85,
            status: 'Completed',
            total_elements: 15420,
            validated_elements: 13847,
            issues: {
              critical: 5,
              warning: 23,
              info: 12
            }
          },
          {
            id: 'sample-2',
            name: 'Residential Complex A',
            filename: 'residential_complex_a.ifc',
            file_size: '89.3 MB',
            upload_date: new Date(Date.now() - 24*60*60*1000).toISOString(),
            health_score: 72,
            status: 'Completed',
            total_elements: 8934,
            validated_elements: 7856,
            issues: {
              critical: 12,
              warning: 45,
              info: 28
            }
          }
        ];
        setProjects(sampleProjects);
        setSelectedProject(sampleProjects[0]);
      }
    } catch (error) {
      console.error('Error loading projects:', error);
      setProjects([]);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectSelect = (project) => {
    setSelectedProject(project);
  };

  const handleFileUpload = async (file, onProgress) => {
    try {
      setLoading(true);

      // Simulate upload progress for demo
      let progress = 0;
      const uploadInterval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 100) progress = 100;
        if (onProgress) onProgress(Math.min(progress, 100));

        if (progress >= 100) {
          clearInterval(uploadInterval);
        }
      }, 200);

      try {
        const result = await apiService.uploadFile(file, onProgress);
        clearInterval(uploadInterval);

        // Reload projects to include new upload
        await loadProjects();

        // Switch to dashboard to see results
        setCurrentView('dashboard');

        return result;
      } catch (apiError) {
        clearInterval(uploadInterval);

        // Create mock upload result for demo
        const mockProject = {
          id: 'demo-' + Date.now(),
          name: file.name.replace(/\.ifc$/i, ''),
          filename: file.name,
          file_size: `${(file.size / (1024*1024)).toFixed(1)} MB`,
          upload_date: new Date().toISOString(),
          health_score: Math.floor(Math.random() * 30) + 60, // 60-90
          status: 'Completed',
          total_elements: Math.floor(Math.random() * 10000) + 5000,
          validated_elements: Math.floor(Math.random() * 1000) + 4000,
          issues: {
            critical: Math.floor(Math.random() * 10),
            warning: Math.floor(Math.random() * 50) + 10,
            info: Math.floor(Math.random() * 20) + 5
          }
        };

        setProjects(prev => [mockProject, ...prev]);
        setSelectedProject(mockProject);
        setCurrentView('dashboard');

        return { message: 'File uploaded successfully (demo mode)', project_id: mockProject.id };
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return (
          <Dashboard 
            projects={projects}
            selectedProject={selectedProject}
            onProjectSelect={handleProjectSelect}
          />
        );

      case 'upload':
        return (
          <FileUpload 
            onFileUpload={handleFileUpload}
            onSuccess={() => setCurrentView('dashboard')}
          />
        );

      case 'issues':
        return (
          <IssuesList 
            project={selectedProject}
            projects={projects}
            onProjectSelect={handleProjectSelect}
          />
        );

      case 'viewer':
        return (
          <ModelViewer 
            project={selectedProject}
          />
        );

      default:
        return (
          <Dashboard 
            projects={projects} 
            selectedProject={selectedProject}
            onProjectSelect={handleProjectSelect}
          />
        );
    }
  };

  if (loading && projects.length === 0) {
    return <Loading message="Loading IFC Dashboard..." />;
  }

  return (
    <div className="app">
      <Header 
        currentView={currentView}
        selectedProject={selectedProject}
        isMobile={isMobile}
      />

      <main className="main-content">
        {renderCurrentView()}
      </main>

      <Navigation 
        currentView={currentView}
        onViewChange={setCurrentView}
        isMobile={isMobile}
      />

      {loading && (
        <div className="loading-overlay">
          <Loading message="Processing..." />
        </div>
      )}
    </div>
  );
}

export default App;