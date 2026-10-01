import {
    Upload,
    Brain,
    TrendingUp,
  } from "lucide-react";
  
  function HowItWorks() {
    const steps = [
      {
        number: "01",
        icon: Upload,
        title: "Upload Your Resume",
        description:
          "Upload your resume and let our system prepare it for intelligent analysis.",
      },
      {
        number: "02",
        icon: Brain,
        title: "AI Analyzes It",
        description:
          "Our AI analyzes your skills, experience, education, keywords, and ATS compatibility.",
      },
      {
        number: "03",
        icon: TrendingUp,
        title: "Get Career Insights",
        description:
          "Receive your resume score, improvement suggestions, missing skills, and job matches.",
      },
    ];
  
    return (
      <section id="how-it-works" className="how-it-works-section">
  
        <div className="section-heading">
          <p className="section-badge">Simple Process</p>
  
          <h2>How It Works</h2>
  
          <p>
            Analyze your resume and get actionable career insights
            in just a few simple steps.
          </p>
        </div>
  
        <div className="steps-container">
          {steps.map((step) => {
            const Icon = step.icon;
  
            return (
              <div className="step-card" key={step.number}>
  
                <div className="step-number">
                  {step.number}
                </div>
  
                <div className="step-icon">
                  <Icon size={30} />
                </div>
  
                <h3>{step.title}</h3>
  
                <p>{step.description}</p>
  
              </div>
            );
          })}
        </div>
  
      </section>
    );
  }
  
  export default HowItWorks;