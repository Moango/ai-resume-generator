import React, { useState } from 'react';
import InputForm from './components/InputForm';
import ResumeDisplay from './components/ResumeDisplay';
import Modal from './components/Modal';
import EditSectionForm from './components/EditSectionForm';
import { sectionNames } from './constants/resumeSections';
import axios from 'axios';

function App() {
  const [resume, setResume] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [editingSection, setEditingSection] = useState(null);
  const [editingSectionValue, setEditingSectionValue] = useState(null);

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/v1/generate_resume', formData);
      setResume(response.data.resume);
    } catch (error) {
      console.error('Error generating resume:', error);
      if (error.response) {
        setError(`服务器错误: ${error.response.status} ${JSON.stringify(error.response.data)}`);
      } else if (error.request) {
        setError('无法连接到服务器，请检查后端是否运行');
      } else {
        setError(`发生错误: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSectionEdit = (section, currentValue) => {
    setEditingSection(section);
    setEditingSectionValue(currentValue);
  };

  const handleEditSubmit = async (modificationRequest) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('/api/v1/modify_resume', {
        current_resume: resume,
        section: editingSection,
        modification_request: modificationRequest
      });
      
      setResume(response.data.resume);
      setEditingSection(null);
      setEditingSectionValue(null);
    } catch (error) {
      console.error('Error modifying resume:', error);
      setError(`修改简历时发生错误: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditCancel = () => {
    setEditingSection(null);
    setEditingSectionValue(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="card bg-gradient-to-r from-primary-50 to-primary-100 mb-8">
          <h1 className="text-3xl font-bold text-primary-900 mb-4">
            定制简历生成系统
          </h1>
          <p className="text-gray-700">
          基于AI的智能简历定制系统，通过分析用户的个人背景（包括技术栈、项目经验等）以及目标公司的招聘需求，自动生成一份与职位JD高度匹配的专业简历。
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="card">
            <InputForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>

          <div>
            {error ? (
              <div className="card bg-red-50 border-l-4 border-red-500">
                <p className="text-red-700">{error}</p>
              </div>
            ) : (
              <ResumeDisplay 
                resume={resume} 
                loading={isLoading} 
                onSectionEdit={handleSectionEdit}
              />
            )}
          </div>
        </div>
      </main>

      <footer className="mt-12 bg-gray-50 border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center text-gray-500">
          定制简历生成系统 ©{new Date().getFullYear()}
        </div>
      </footer>

      <Modal
        isOpen={!!editingSection}
        onClose={handleEditCancel}
        title={`修改${editingSection ? sectionNames[editingSection] : ''}`}
      >
        <EditSectionForm
          section={editingSection}
          currentValue={editingSectionValue}
          onSubmit={handleEditSubmit}
          onCancel={handleEditCancel}
        />
      </Modal>
    </div>
  );
}

export default App;
