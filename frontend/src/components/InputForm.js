import React, { useRef, useEffect } from 'react';

import './InputForm.css';


function InputForm({ onSubmit, isLoading }) {
  const personalInfoRef = useRef(null);
  const jobDescriptionRef = useRef(null);

  const adjustTextareaHeight = (textarea) => {
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  };

  useEffect(() => {
    adjustTextareaHeight(personalInfoRef.current);
    adjustTextareaHeight(jobDescriptionRef.current);
  }, []);

  const handleInput = (e) => {
    adjustTextareaHeight(e.target);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = {
      personal_info: e.target.personalInfo.value,
      job_description: e.target.jobDescription.value,
      position_name: e.target.positionName.value,
    };
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label 
          htmlFor="positionName" 
          className="block text-lg font-medium text-gray-700 mb-2"
        >
          目标职位
        </label>
        <input
          type="text"
          id="positionName"
          name="positionName"
          className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white/50 backdrop-blur-sm transition duration-200"
          placeholder="请输入目标职位名称"
          required
        />
      </div>

      <div>
        <label 
          htmlFor="personalInfo" 
          className="block text-lg font-medium text-gray-700 mb-2"
        >
          个人信息
        </label>
        <textarea
          id="personalInfo"
          name="personalInfo"
          ref={personalInfoRef}
          onInput={handleInput}
          className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white/50 backdrop-blur-sm transition duration-200 min-h-[150px]"
          placeholder="请输入您的教育背景、工作经验、技能等相关信息"
          required
        />
      </div>

      <div>
        <label 
          htmlFor="jobDescription" 
          className="block text-lg font-medium text-gray-700 mb-2"
        >
          职位描述
        </label>
        <textarea
          id="jobDescription"
          name="jobDescription"
          ref={jobDescriptionRef}
          onInput={handleInput}
          className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white/50 backdrop-blur-sm transition duration-200 min-h-[150px]"
          placeholder="请输入目标职位的描述和要求"
          required
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-4 px-6 rounded-lg text-white font-semibold text-lg
          ${isLoading 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 transform hover:-translate-y-0.5'
          } transition duration-200 shadow-lg`}
      >
        {isLoading ? (
          <div className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            正在生成简历...
          </div>
        ) : '生成简历'}
      </button>
    </form>
  );
}

export default InputForm;
