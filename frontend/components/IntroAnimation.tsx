"use client";

import { useState } from "react";
import Image from "next/image";

interface IntroAnimationProps {
  onComplete: () => void;
}

export default function IntroAnimation({ onComplete }: IntroAnimationProps) {
  const [isExiting, setIsExiting] = useState(false);

  const handleComplete = () => {
    setIsExiting(true);
    setTimeout(() => {
      onComplete();
    }, 500);
  };

  return (
    <div className={`intro-overlay ${isExiting ? 'intro-exit' : ''}`}>
      <div className="intro-container">
        {/* Logo Section */}
        <div className="intro-logo">
          <div className="logo-wrapper">
            <Image
              src="/logo1.png"
              alt="Kaabil Lens Logo"
              width={350}
              height={300}
              className="object-contain drop-shadow-2xl"
              priority
            />
          </div>
        </div>

        {/* Title Section */}
        <div className="intro-title">
          <h1 className="main-title">
            <span className="title-text-gradient">Kaabil Lens</span>
          </h1>
          <p className="subtitle">
            Intelligent Resume Screening & Candidate Ranking
          </p>
        </div>

        {/* Get Started Button */}
        <div className="intro-button">
          <button
            onClick={handleComplete}
            className="get-started-btn"
          >
            <span className="btn-text">Get Started</span>
            <span className="btn-arrow">→</span>
            <div className="btn-glow"></div>
          </button>
          <p className="hover-hint hint-show">Click to enter the platform</p>
        </div>
      </div>

      {/* Decorative Elements - Cyan Orbs */}
      <div className="intro-decorations">
        <div className="orb orb-1"></div>
        <div className="orb orb-2"></div>
        <div className="orb orb-3"></div>
        <div className="grid-lines"></div>
      </div>
    </div>
  );
}

