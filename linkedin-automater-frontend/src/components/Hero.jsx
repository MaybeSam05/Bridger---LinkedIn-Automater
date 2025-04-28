import React from "react";

const conversations = "text-4xl md:text-5xl font-bold text-slate-700 mb-4";
const outreach = "text-slate-600 ";
const easy = "text-4xl md:text-5xl font-bold mb-6";

const Hero = () => {
  return (
    <section className="bg-gradient-to-b from-gray-300 to-white py-16 md:py-24">
      <div className="container mx-auto px-6 md:px-12 flex flex-col lg:flex-row items-center justify-between">
        
        {/* Left Side Text */}
        <div className="lg:w-1/2 lg:mr-12 mb-12 lg:mb-0">
          <h1 className= { conversations } style = {{ color: "#2C3E50"}} >
            More conversations,<br />
            <span className= { outreach } style = {{ color: "#2C3E50"}} >less outreach.</span>
          </h1><br />
          <h2 className= { easy } style = {{ color: "#0F689C"}} >
            Bridger makes it easy.
          </h2>
        </div>

        {/* Right Side Image */}
        <div className="lg:w-1/2">
          <div className="relative">
            <img
              src="/laptopzoomBG.png"
              alt="Laptop Mockup"
              className="w-full h-auto object-contain rounded-lg"
            />
          </div>
        </div>

      </div>
    </section>
  );
};

export default Hero;
