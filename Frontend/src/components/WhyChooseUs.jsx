import {
    CheckCircle2,
    Sparkles,
  } from "lucide-react";
  
  function WhyChooseUs() {
    const benefits = [
      "Understand your resume strengths and weaknesses",
      "Improve your ATS compatibility",
      "Identify missing and relevant skills",
      "Get practical AI-powered recommendations",
      "Match your resume with job descriptions",
    ];
  
    return (
      <section className="why-section">
  
        <div className="why-content">
  
          <p className="section-badge">
            Smarter Career Decisions
          </p>
  
          <h2>
            Turn Your Resume Into a Career Advantage
          </h2>
  
          <p className="why-description">
            ResumeAI helps you understand what is working in your
            resume and what needs improvement, so you can apply
            with greater confidence.
          </p>
  
          <div className="benefits-list">
            {benefits.map((benefit) => (
              <div className="benefit-item" key={benefit}>
                <CheckCircle2 size={22} />
                <span>{benefit}</span>
              </div>
            ))}
          </div>
  
        </div>
  
        <div className="why-highlight">
  
          <div className="highlight-icon">
            <Sparkles size={34} />
          </div>
  
          <h3>AI-Powered Insights</h3>
  
          <p>
            Get personalized feedback based on the content
            and requirements of your resume.
          </p>
  
        </div>
  
      </section>
    );
  }
  
  export default WhyChooseUs;