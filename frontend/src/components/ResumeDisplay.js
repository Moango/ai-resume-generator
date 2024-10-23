import React from 'react';
import './ResumeDisplay.css';

function ResumeDisplay({ resume, loading }) {
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

  let resumeData;
  try {
    resumeData = JSON.parse(resume);
  } catch (error) {
    console.error('Error parsing resume JSON:', error);
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
        <p className="text-red-700">简历数据格式错误</p>
      </div>
    );
  }

  const renderValue = (value) => {
    if (Array.isArray(value)) {
      return (
        <ul className="list-disc list-inside space-y-1">
          {value.map((item, index) => (
            <li key={index} className="text-gray-600">
              {typeof item === 'object' ? renderObject(item) : item}
            </li>
          ))}
        </ul>
      );
    } else if (typeof value === 'object' && value !== null) {
      return renderObject(value);
    } else {
      return <span className="text-gray-600">{value}</span>;
    }
  };

  const renderObject = (obj) => {
    if (!obj) return null;
    
    return (
      <div className="space-y-2">
        {Object.entries(obj).map(([key, value]) => (
          <div key={key} className="space-y-1">
            <div className="font-medium text-gray-700 capitalize">
              {key.replace(/_/g, ' ')}
            </div>
            <div className="ml-4">{renderValue(value)}</div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8 space-y-6">
      {Object.entries(resumeData).map(([section, content]) => (
        <div key={section} className="border-b border-gray-200 pb-6 last:border-0">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 capitalize">
            {section.replace(/_/g, ' ')}
          </h3>
          {renderValue(content)}
        </div>
      ))}
    </div>
  );
}

export default ResumeDisplay;
