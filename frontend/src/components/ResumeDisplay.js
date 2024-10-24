import React from 'react';
import ReactMarkdown from 'react-markdown';
import { sectionNames } from '../constants/resumeSections';
import './ResumeDisplay.css';

function ResumeDisplay({ resume, loading, onSectionEdit }) {
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px] bg-white/50 backdrop-blur-sm rounded-lg p-8">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
          <p className="mt-4 text-gray-600">正在生成简历...</p>
        </div>
      </div>
    );
  }

  if (!resume) {
    return (
      <div className="min-h-[400px] bg-white/50 backdrop-blur-sm rounded-lg p-8 flex items-center justify-center">
        <p className="text-gray-500 text-lg">请在左侧输入信息以生成简历</p>
      </div>
    );
  }

  // 将简历内容分成不同的部分
  const sections = resume.split(/(?=^# |\n## )/m).filter(Boolean);

  return (
    <div className="resume-container prose prose-sm max-w-none">
      {sections.map((section, index) => {
        const sectionTitle = section.match(/^#+ (.*)/m)?.[1];
        const sectionKey = Object.entries(sectionNames).find(
          ([_, value]) => value === sectionTitle
        )?.[0];

        return (
          <div key={index} className="resume-section relative group">
            <ReactMarkdown>{section}</ReactMarkdown>
            {sectionKey && (
              <button
                onClick={() => onSectionEdit(sectionKey, section)}
                className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 
                         transition-opacity duration-200 bg-blue-500 text-white 
                         px-2 py-1 rounded text-sm"
              >
                修改此部分
              </button>
            )}
          </div>
        );
      })}
    </div>
  );
}

export default ResumeDisplay;
