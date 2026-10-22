import HowItWorks from "../components/HowItWorks";
import Features from "../components/Features";
import WhyChooseUs from "../components/WhyChooseUs";
import FinalCTA from "../components/FinalCTA";
function Home() {
    return (
      <div className="home-page">
  
        {/* Hero Section */}
        <section className="hero-section">
  
          <div className="hero-content">
  
            <p className="hero-badge">
              AI-Powered Career Assistant
            </p>
  
            <h1>
              Build a Resume That
              <span> Gets Noticed.</span>
            </h1>
  
            <p className="hero-description">
              Analyze your resume with AI-powered insights, improve your
              ATS score, identify missing skills, and find jobs that match
              your profile.
            </p>
  
            <div className="hero-buttons">
              <a href="/signup" className="hero-primary-btn">
                Analyze My Resume
              </a>
  
              <a href="#how-it-works" className="hero-secondary-btn">
                How It Works
              </a>
            </div>
  
          </div>
  
          <div className="hero-image-container">
            <img
              src="/src/assets/hero.png"
              alt="AI Resume Analysis"
              className="hero-image"
            />
          </div>
  
        </section>

        <HowItWorks />

        <Features />

        <WhyChooseUs />

        <FinalCTA />
  
      </div>
    );
  }
  
  export default Home;