import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

function EditSectionForm({ section, currentValue, onSubmit, onCancel }) {
  const [modificationRequest, setModificationRequest] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(modificationRequest);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          当前内容：
        </label>
        <div className="p-3 bg-gray-50 rounded-lg prose prose-sm max-w-none">
          <ReactMarkdown>{currentValue}</ReactMarkdown>
        </div>
      </div>

      <div>
        <label htmlFor="modification" className="block text-sm font-medium text-gray-700 mb-2">
          修改要求：
        </label>
        <textarea
          id="modification"
          value={modificationRequest}
          onChange={(e) => setModificationRequest(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          rows={4}
          placeholder="请输入您的修改要求..."
          required
        />
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
        >
          取消
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors duration-200"
        >
          确认修改
        </button>
      </div>
    </form>
  );
}

export default EditSectionForm;
