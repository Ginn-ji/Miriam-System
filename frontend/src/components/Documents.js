import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { FileText, Upload, Search } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

export const Documents = () => {
  const { t } = useLanguage();
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await apiClient.get('/documents');
      setDocuments(response.data.documents || []);
    } catch (error) {
      console.error('Error fetching documents:', error);
      toast.error('Failed to load documents');
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await apiClient.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('Document uploaded successfully');
      fetchDocuments();
    } catch (error) {
      console.error('Error uploading document:', error);
      toast.error('Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  const filteredDocuments = documents.filter((doc) =>
    doc.filename.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6" data-testid="documents-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-serif font-bold tracking-tight text-primary" data-testid="documents-title">
            {t('documents')}
          </h1>
          <p className="text-muted-foreground mt-1">Upload and manage legal documents</p>
        </div>
        <label htmlFor="file-upload">
          <Button disabled={uploading} className="cursor-pointer" data-testid="upload-btn">
            <Upload className="h-4 w-4 mr-2" />
            {uploading ? 'Uploading...' : t('uploadDocument')}
          </Button>
          <Input
            id="file-upload"
            type="file"
            accept=".pdf,.txt"
            onChange={handleFileUpload}
            className="hidden"
          />
        </label>
      </div>

      <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Search className="h-5 w-5 text-muted-foreground" />
            <Input
              placeholder="Search documents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="max-w-sm"
              data-testid="search-input"
            />
          </div>
        </CardHeader>
        <CardContent>
          {filteredDocuments.length > 0 ? (
            <div className="space-y-2">
              {filteredDocuments.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center justify-between p-4 rounded-sm border hover:bg-muted/50 transition-colors"
                  data-testid="document-item"
                >
                  <div className="flex items-center gap-3">
                    <FileText className="h-5 w-5 text-primary" />
                    <div>
                      <p className="font-medium">{doc.filename}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="legal-badge">{doc.language}</span>
                        <span className="text-xs text-muted-foreground">
                          {new Date(doc.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12" data-testid="empty-documents">
              <FileText className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">{t('noDocuments')}</p>
              <p className="text-sm text-muted-foreground mt-1">{t('dragDrop')}</p>
              <p className="text-xs text-muted-foreground mt-2">{t('supportedFormats')}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};