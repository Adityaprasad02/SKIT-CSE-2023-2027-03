import {
    BarChart3,
    Brain,
    Wrench,
    Target,
    Lightbulb,
    FileSearch,
  } from "lucide-react";
  
  function Features() {
    const features = [
      {
        icon: BarChart3,
        title: "ATS Score",
        description:
          "Check how well your resume performs against Applicant Tracking Systems.",
      },
      {
        icon: Brain,
        title: "AI Resume Analysis",
        description:
          "Get an AI-powered analysis of your resume content, structure, and quality.",
      },
      {
        icon: Wrench,
        title: "Skill Analysis",
        description:
          "Identify your key skills and discover important skills that may be missing.",
      },
      {
        icon: Target,
        title: "Job Matching",
        description:
          "Compare your resume with job descriptions and discover relevant opportunities.",
      },
      {
        icon: Lightbulb,
        title: "AI Suggestions",
        description:
          "Receive practical suggestions to improve your resume and make it more effective.",
      },
      {
        icon: FileSearch,
        title: "Resume Insights",
        description:
          "Understand your resume strengths, weaknesses, keywords, and improvement areas.",
      },
    ];
  
    return (
      <section id="features" className="features-section">
  
        <div className="section-heading">
          <p className="section-badge">Powerful Features</p>
  
          <h2>Everything You Need to Improve Your Resume</h2>
  
          <p>
            Our AI-powered platform helps you understand your resume,
            improve it, and find better opportunities.
          </p>
        </div>
  
        <div className="features-container">
          {features.map((feature) => {
            const Icon = feature.icon;
  
            return (
              <div className="feature-card" key={feature.title}>
  
                <div className="feature-icon">
                  <Icon size={28} />
                </div>
  
                <h3>{feature.title}</h3>
  
                <p>{feature.description}</p>
  
              </div>
            );
          })}
        </div>
  
      </section>
    );
  }
  
  export default Features;