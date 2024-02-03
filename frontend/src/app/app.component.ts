import { Component } from '@angular/core';
import { HttpClient,HttpHeaders} from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.css']
})
export class AppComponent {
  title='frontend'
  selectedFile: File | null = null;
  fileUrl: SafeResourceUrl | null = null;

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
    this.createFileUrl();
  }

  createFileUrl(): void {
    if (this.selectedFile) {
      const objectUrl = URL.createObjectURL(this.selectedFile);
      // Sanitize the URL
      this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
    }
  }

  onUpload(): void {
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      this.http.post('http://your-flask-api-endpoint', formData)
        .subscribe(response => {
          console.log('File uploaded successfully:', response);
          // Handle the response from the server
        }, error => {
          console.error('Error uploading file:', error);
          // Handle errors
        });
    }
  }
}
