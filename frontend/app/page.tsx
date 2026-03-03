"use client";

import { useState, useEffect } from "react";
import { uploadResumes, analyzeJobDescription } from "@/lib/api";
import { Toaster, toast } from "react-hot-toast";
import dynamic from "next/dynamic";
import { FiUpload, FiDownload } from "react-icons/fi";
import Image from "next/image";
import IntroAnimation from "@/components/IntroAnimation";

interface Candidate {
  Rank: number;
  Candidate: string;
  "Skill Match (%)": number;
  "Experience Match (%)": number;
  "Final Score": number;
  "Matched Skills": string;
  "Missing Skills": string;
}

const ScoreOverviewChart = dynamic(
  () => import("@/components/ScoreOverviewChart").then((mod) => mod.default),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-[260px] items-center justify-center text-sm text-cyan-400">
        Loading score chart…
      </div>
    ),
  }
);

export default function HomePage() {
  const [showIntro, setShowIntro] = useState(true);
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [jdText, setJdText] = useState("");
  const [jobProcessed, setJobProcessed] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [resumesAnalyzed, setResumesAnalyzed] = useState(false);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(false);
  const [expandedCandidate, setExpandedCandidate] = useState<number | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  // Handle intro animation complete
  const handleIntroComplete = () => {
    setShowIntro(false);
  };

  // Animation trigger
  const [animated, setAnimated] = useState(false);
  useEffect(() => {
    setAnimated(true);
  }, []);

  // Step 1: Analyze Job Description
  const handleAnalyzeJD = async () => {
    if (!jdText.trim()) {
      toast.error("Please enter a job description");
      return;
    }
    setLoading(true);
    setStatusMessage("Analyzing job description…");
    try {
      await analyzeJobDescription(jdText);
      setJobProcessed(true);
      toast.success("Job Description analyzed successfully!");
      setStatusMessage("Job description analyzed successfully. You can now upload resumes.");
      setTimeout(() => setStep(2), 500);
    } catch (err) {
      console.error(err);
      toast.error("Failed to analyze Job Description");
      setStatusMessage("Failed to analyze job description. Please try again.");
    } finally {
      setLoading(false);
      setTimeout(() => setStatusMessage(null), 4000);
    }
  };

  // Step 2: Upload & Score Resumes
  const handleUpload = async () => {
    if (!files.length) {
      toast.error("Please select at least one resume");
      return;
    }
    setLoading(true);
    setStatusMessage(`Uploading and scoring ${files.length} resume${files.length > 1 ? "s" : ""}…`);
    try {
      const res = await uploadResumes(files);
      setCandidates(res.ranked_candidates || []);
      setResumesAnalyzed(true);
      toast.success("Resumes scored successfully!");
      setStatusMessage("Resumes scored successfully. Review the ranked candidates below.");
      setTimeout(() => setStep(3), 500);
    } catch (err) {
      console.error(err);
      toast.error("Resume upload/scoring failed");
      setStatusMessage("Resume upload or scoring failed. Please check your connection and try again.");
    } finally {
      setLoading(false);
      setTimeout(() => setStatusMessage(null), 4000);
    }
  };

  // CSV Download
  const handleDownloadCSV = () => {
    if (!candidates.length) return;
    const csvContent =
      "data:text/csv;charset=utf-8," +
      [
        Object.keys(candidates[0]).join(","),
        ...candidates.map((c) =>
          Object.values(c)
            .map((v) => `"${v}"`)
            .join(",")
        ),
      ].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "ranked_candidates.csv");
    document.body.appendChild(link);
    link.click();
    link.remove();
    toast.success("CSV downloaded!");
  };

  // Prepare chart data
  const chartData = candidates.slice(0, 10).map((c) => ({
    name: c.Candidate.substring(0, 15),
    "Final Score": c["Final Score"],
    "Skill Match": c["Skill Match (%)"],
    "Experience Match": c["Experience Match (%)"],
  }));

  return (
    <>
      {showIntro && <IntroAnimation onComplete={handleIntroComplete} />}
      
      <div className={`min-h-screen bg-gradient-to-br from-navy-deep via-navy-dark to-navy-deep text-cyan-50 overflow-x-hidden ${showIntro ? 'hidden' : ''}`}>
      {/* Ambient Lighting Effects */}
      <div className="ambient-light ambient-light-1"></div>
      <div className="ambient-light ambient-light-2"></div>
      <div className="ambient-light ambient-light-3"></div>
      <div className="lens-flare"></div>
      <div className="lens-flare-2"></div>
      <div className="ambient-occlusion"></div>
      
      <Toaster position="top-right" />

      {/* Navigation Dots */}
      <nav
        aria-label="Wizard steps"
        className="fixed right-6 top-1/2 z-40 hidden -translate-y-1/2 flex-col gap-6 lg:flex"
      >
        {[1, 2, 3].map((s) => {
          const isCurrent = step === s;
          const isDisabled = step < s;
          return (
            <button
              key={s}
              type="button"
              onClick={() => !isDisabled && setStep(s as 1 | 2 | 3)}
              aria-label={`Go to step ${s}`}
              aria-current={isCurrent ? "step" : undefined}
              aria-disabled={isDisabled}
              className={`h-4 w-4 rounded-full border outline-none transition-all focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-navy-deep ${
                isCurrent
                  ? "bg-cyan-500 shadow-lg shadow-cyan-500/60 border-cyan-400"
                  : isDisabled
                  ? "bg-cyan-900/60 border-cyan-800"
                  : "bg-cyan-700 hover:bg-cyan-600 border-cyan-600"
              }`}
            />
          );
        })}
      </nav>

      {/* Header */}
      <header className="bg-gradient-to-r from-navy-dark via-navy-light to-navy-dark p-6 shadow-lg border-b border-cyan-500/20">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-8">
          <div className="flex items-center gap-1">
            {/* Logo */}
            <div className="h-20 w-40 relative">
              <Image 
                src="/logo1.png" 
                alt="Kaabil Lens Logo" 
                width={300} 
                height={300}
                className="object-contain"
              />
            </div>
            <div>
              <h1 className="mb-1 text-3xl font-bold tracking-tight text-white sm:text-4xl neon-cyan">
                Kaabil Lens
              </h1>
              <p className="max-w-xl text-sm text-cyan-300 sm:text-base">
                Intelligent Resume Screening & Candidate Ranking
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Step Indicator */}
      <section className="border-b border-cyan-500/20 bg-navy-deep/60 backdrop-blur">
        <div className="mx-auto flex max-w-5xl flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex flex-1 items-center justify-between">
            {[
              { num: 1, label: "Job Description" },
              { num: 2, label: "Upload Resumes" },
              { num: 3, label: "Results" },
            ].map((s, idx) => (
              <div key={s.num} className="flex flex-1 items-center">
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-full text-sm font-semibold transition-all sm:h-12 sm:w-12 ${
                    step >= s.num
                      ? "bg-gradient-to-br from-cyan-500 to-cyan-400 text-white shadow-lg shadow-cyan-500/50"
                      : "bg-cyan-900/50 text-cyan-400"
                  }`}
                >
                  {step > s.num ? "✓" : s.num}
                </div>
                <div
                  className={`ml-3 ${
                    step >= s.num ? "text-white" : "text-cyan-400"
                  }`}
                >
                  <p className="text-xs font-medium uppercase tracking-wide sm:text-sm">
                    {s.label}
                  </p>
                </div>
                {idx < 2 && (
                  <div
                    className={`mx-4 hidden h-1 flex-1 rounded-full sm:block ${
                      step > s.num ? "bg-gradient-to-r from-cyan-500 to-cyan-400" : "bg-cyan-900/50"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
          <div
            aria-live="polite"
            className="mt-2 text-xs text-cyan-300 sm:mt-0 sm:text-sm"
          >
            {step === 1 && "Step 1 of 3: Provide the job description for analysis."}
            {step === 2 && "Step 2 of 3: Upload candidate resumes as PDFs for scoring."}
            {step === 3 && "Step 3 of 3: Review ranked candidates and export results."}
          </div>
        </div>
      </section>

      {/* Content */}
      <main
        id="main-content"
        className="mx-auto flex max-w-5xl flex-col gap-6 px-4 py-8 sm:py-10"
        aria-busy={loading}
      >
        {statusMessage && (
          <div
            aria-live="polite"
            className="rounded-lg border border-cyan-500/30 bg-navy-dark/70 px-4 py-3 text-sm text-cyan-100 shadow-sm shadow-cyan-500/10"
          >
            {statusMessage}
          </div>
        )}
        
        {/* Step 1: Job Description */}
        {step === 1 && (
          <div
            className={`animate-fadeIn transition-all duration-500 ${
              animated ? "opacity-100" : "opacity-0"
            }`}
          >
            <section
              aria-label="Job description analysis"
              className="glass-card neon-rim rounded-2xl border border-cyan-500/20 bg-navy-dark/70 p-6 shadow-xl sm:p-8 elevation-3"
            >
              <header className="mb-4 flex flex-col gap-2 sm:mb-6 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-white sm:text-2xl">
                    📄 Enter Job Description
                  </h2>
                  <p className="mt-1 text-xs text-cyan-300 sm:text-sm">
                    Paste the role requirements so the engine understands what a strong
                    candidate looks like.
                  </p>
                </div>
                {jobProcessed && (
                  <span className="mt-2 inline-flex items-center rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300 sm:mt-0">
                    ✓ Job analyzed
                  </span>
                )}
              </header>

              <label className="mb-2 block text-sm font-medium text-cyan-100">
                Job description
                <span className="ml-1 text-xs text-cyan-400">(required)</span>
              </label>
              <textarea
                className="mb-4 h-56 w-full resize-none rounded-lg border border-cyan-500/30 bg-navy-deep/60 p-4 text-sm text-cyan-50 outline-none ring-0 transition-all placeholder:text-cyan-500/50 focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/50 overflow-y-auto"
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                placeholder="Paste the complete job description here, including responsibilities, required skills, and experience."
              />

              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs text-cyan-400 sm:text-sm">
                  We send the text securely to your backend API for analysis. No format is
                  required—just paste what you already share with candidates.
                </p>
                <button
                  type="button"
                  onClick={handleAnalyzeJD}
                  disabled={loading}
                  className={`btn-float inline-flex items-center justify-center rounded-lg px-5 py-2.5 text-sm font-semibold text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-navy-deep ${
                    loading
                      ? "cursor-not-allowed bg-cyan-900"
                      : "bg-gradient-to-r from-cyan-600 to-cyan-500 hover:shadow-lg hover:shadow-cyan-500/40"
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-cyan-200 border-t-transparent" />
                      Analyzing…
                    </span>
                  ) : (
                    "Analyze job description"
                  )}
                </button>
              </div>
            </section>
          </div>
        )}

        {/* Step 2: Upload Resumes */}
        {step === 2 && (
          <div
            className={`animate-fadeIn transition-all duration-500 ${
              animated ? "opacity-100" : "opacity-0"
            }`}
          >
            <section
              aria-label="Upload resumes for scoring"
              className="glass-card neon-rim rounded-2xl border border-cyan-500/20 bg-navy-dark/70 p-6 shadow-xl sm:p-8 elevation-3"
            >
              <header className="mb-4 flex flex-col gap-2 sm:mb-6 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-white sm:text-2xl">
                    📤 Upload Resumes
                  </h2>
                  <p className="mt-1 text-xs text-cyan-300 sm:text-sm">
                    Upload one or more candidate resumes as PDF files. We&apos;ll score them
                    against the analyzed job description.
                  </p>
                </div>
                {resumesAnalyzed && (
                  <span className="mt-2 inline-flex items-center rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300 sm:mt-0">
                    ✓ Resumes scored
                  </span>
                )}
              </header>

              {/* File Upload Area */}
              <div className="glass-card mb-6 rounded-xl border-2 border-dashed border-cyan-500/30 bg-navy-deep/40 p-8 text-center transition-colors hover:border-cyan-400 hover:bg-navy-deep/60 hover:shadow-lg hover:shadow-cyan-500/20">
                <input
                  type="file"
                  id="file-input"
                  multiple
                  accept=".pdf"
                  onChange={(e) =>
                    e.target.files && setFiles(Array.from(e.target.files))
                  }
                  className="hidden"
                />
                <label
                  htmlFor="file-input"
                  className="flex cursor-pointer flex-col items-center gap-3"
                >
                  <span className="text-4xl" aria-hidden="true">
                    📎
                  </span>
                  <span className="font-semibold text-white">
                    Click to select files or drag &amp; drop PDFs
                  </span>
                  <span className="text-sm text-cyan-400">
                    PDF files only
                  </span>
                </label>
              </div>

              {/* File List */}
              {files.length > 0 && (
                <div className="mb-6">
                  <h3 className="mb-2 text-sm font-semibold text-white sm:mb-3">
                    Selected Files ({files.length}):
                  </h3>
                  <div className="grid gap-2">
                    {files.map((f) => (
                      <div
                        key={f.name}
                        className="flex items-center gap-2 rounded border border-cyan-500/30 bg-navy-deep/80 px-3 py-2 text-left text-xs text-cyan-100 sm:text-sm"
                      >
                        <span className="text-cyan-400" aria-hidden="true">
                          ✓
                        </span>
                        <span className="truncate">{f.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <button
                type="button"
                onClick={handleUpload}
                disabled={loading || !files.length}
                className={`btn-float inline-flex w-full items-center justify-center rounded-lg px-5 py-2.5 text-sm font-semibold text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 focus-visible:ring-offset-2 focus-visible:ring-offset-navy-deep ${
                  loading || !files.length
                    ? "bg-cyan-900 cursor-not-allowed"
                    : "bg-gradient-to-r from-emerald-600 to-cyan-600 hover:shadow-lg hover:shadow-emerald-500/40"
                }`}
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-emerald-200 border-t-transparent" />
                    Processing resumes…
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                    <FiUpload className="icon-inline" /> Upload & Score Resumes
                  </span>
                )}
              </button>
            </section>
          </div>
        )}

        {/* Step 3: Results */}
        {step === 3 && (
          <div
            className={`animate-fadeIn transition-all duration-500 ${
              animated ? "opacity-100" : "opacity-0"
            }`}
          >
            {candidates.length ? (
              <section
                aria-label="Scored candidates and visualizations"
                className="space-y-8"
              >
                {/* Score Chart */}
                <div className="glass-card neon-rim rounded-2xl border border-cyan-500/20 bg-navy-dark/70 p-6 shadow-xl sm:p-8 elevation-3">
                  <h3 className="mb-4 text-lg font-semibold text-white sm:mb-6 sm:text-xl">
                    📊 Score Overview
                  </h3>
                  <ScoreOverviewChart data={chartData} />
                </div>

                {/* Candidate Cards */}
                <div>
                  <h3 className="mb-4 text-2xl font-bold text-white sm:mb-6">
                    🏆 Top Candidates
                  </h3>
                  <div className="grid gap-4">
                    {candidates.map((candidate, idx) => (
                      <div
                        key={idx}
                        className="glass-card candidate-card neon-rim overflow-hidden rounded-2xl border border-cyan-500/20 bg-navy-dark/80 shadow hover:border-cyan-400 hover:shadow-lg hover:shadow-cyan-500/20 elevation-2"
                      >
                        {/* Header */}
                        <button
                          type="button"
                          onClick={() =>
                            setExpandedCandidate(
                              expandedCandidate === idx ? null : idx
                            )
                          }
                          aria-expanded={expandedCandidate === idx}
                          aria-controls={`candidate-details-${idx}`}
                          className="flex w-full items-center justify-between gap-4 p-5 text-left transition-colors hover:bg-navy-light/50 sm:p-6"
                        >
                          <div className="flex flex-1 items-center gap-4">
                          <div className="rank-badge flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold text-white sm:h-12 sm:w-12 sm:text-base glow-border">
                              {candidate.Rank}
                            </div>
                            <div className="flex-1 text-left">
                              <h4 className="truncate text-sm font-semibold text-white sm:text-lg">
                                {candidate.Candidate}
                              </h4>
                            </div>
                          </div>

                          {/* Score */}
                          <div className="mr-2 text-right sm:mr-4">
                            <div className="text-2xl font-bold neon-cyan sm:text-3xl">
                              {candidate["Final Score"]}
                            </div>
                            <p className="text-xs text-cyan-400 sm:text-sm">
                              Final score
                            </p>
                          </div>

                          {/* Expand Icon */}
                          <span
                            className={`text-xl transition-transform sm:text-2xl ${
                              expandedCandidate === idx ? "rotate-180" : ""
                            }`}
                          >
                            ▼
                          </span>
                        </button>

                        {/* Expandable Details */}
                        {expandedCandidate === idx && (
                          <div
                            id={`candidate-details-${idx}`}
                            className="space-y-4 border-t border-cyan-500/20 bg-navy-deep/60 px-5 py-5 sm:px-6 sm:py-6"
                          >
                            {/* Progress Bars */}
                            <div>
                              <div className="mb-2 flex justify-between">
                                <span className="text-sm font-semibold text-cyan-200">
                                  Skill Match
                                </span>
                                <span className="text-sm font-bold text-cyan-400">
                                  {candidate["Skill Match (%)"]}%
                                </span>
                              </div>
                              <div className="h-2.5 w-full overflow-hidden rounded-full bg-navy-deep">
                                <div
                                  className="progress-bar-skill h-full w-full rounded-full transition-all duration-500"
                                  style={{
                                    width: `${candidate["Skill Match (%)"]}%`,
                                  }}
                                />
                              </div>
                            </div>

                            <div>
                              <div className="mb-2 flex justify-between">
                                <span className="text-sm font-semibold text-cyan-200">
                                  Experience Match
                                </span>
                                <span className="text-sm font-bold text-emerald-400">
                                  {candidate["Experience Match (%)"]}%
                                </span>
                              </div>
                              <div className="h-2.5 w-full overflow-hidden rounded-full bg-navy-deep">
                                <div
                                  className="progress-bar-experience h-full w-full rounded-full transition-all duration-500"
                                  style={{
                                    width: `${candidate["Experience Match (%)"]}%`,
                                  }}
                                />
                              </div>
                            </div>

                            {/* Skills */}
                            <div className="mt-4 grid gap-4 sm:grid-cols-2">
                              <div>
                                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-cyan-400 sm:text-sm">
                                  ✅ Matched Skills:
                                </p>
                                <div className="flex flex-wrap gap-2">
                                  {candidate["Matched Skills"]
                                    .split(",")
                                    .map((skill: string, i: number) => (
                                      <span
                                        key={i}
                                        className="tag-matched inline-flex items-center rounded-full px-3 py-1 text-xs text-emerald-200"
                                      >
                                        {skill.trim()}
                                      </span>
                                    ))}
                                </div>
                              </div>
                              <div>
                                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-cyan-400 sm:text-sm">
                                  ❌ Missing Skills:
                                </p>
                                <div className="flex flex-wrap gap-2">
                                  {candidate["Missing Skills"]
                                    .split(",")
                                    .map((skill: string, i: number) => (
                                      <span
                                        key={i}
                                        className="tag-missing inline-flex items-center rounded-full px-3 py-1 text-xs text-red-200"
                                      >
                                        {skill.trim()}
                                      </span>
                                    ))}
                                </div>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-wrap gap-3 sm:gap-4">
                  <button
                    type="button"
                    onClick={handleDownloadCSV}
                    className="btn-float flex-1 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:shadow-lg hover:shadow-cyan-500/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-navy-deep"
                  >
                    <span className="flex items-center justify-center gap-2">
                      <FiDownload className="icon-inline" /> Download CSV
                    </span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setStep(2);
                      setFiles([]);
                    }}
                    className="btn-float flex-1 rounded-lg bg-navy-light px-4 py-2.5 text-sm font-semibold text-cyan-100 hover:bg-navy-dark hover:shadow-lg hover:shadow-cyan-500/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-navy-deep"
                  >
                    ⬅️ Back to Upload
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setStep(1);
                      setFiles([]);
                      setCandidates([]);
                      setJobProcessed(false);
                      setJdText("");
                    }}
                    className="btn-float flex-1 rounded-lg bg-navy-light px-4 py-2.5 text-sm font-semibold text-cyan-100 hover:bg-navy-dark hover:shadow-lg hover:shadow-cyan-500/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-navy-deep"
                  >
                    🔄 Start Over
                  </button>
                </div>
              </section>
            ) : (
              <section className="glass-card neon-rim rounded-2xl border border-dashed border-cyan-500/30 bg-navy-dark/60 p-10 text-center shadow-inner">
                <p className="text-sm text-cyan-300 sm:text-base">
                  No candidates found yet. Once you analyze a job description and upload
                  resumes, you&apos;ll see a ranked list of candidates here, along with a
                  visual score overview.
                </p>
              </section>
            )}
          </div>
        )}
      </main>
    </div>
    </>
  );
}

