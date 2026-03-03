// frontend/lib/api.ts
export const BASE_URL = "http://localhost:8000";

export async function uploadResumes(files: File[]) {
  const formData = new FormData();

  // append all files with the key "files"
  files.forEach((file) => formData.append("files", file));

  const res = await fetch(`${BASE_URL}/upload-resumes`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

// helper for job description analysis
export async function analyzeJobDescription(jdText: string) {
  const formData = new FormData();
  formData.append("jd_text", jdText);

  const res = await fetch(`${BASE_URL}/analyze-job`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Job analysis failed");
  return res.json();
}