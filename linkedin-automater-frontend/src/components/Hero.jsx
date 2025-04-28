import React from "react";

const Hero = () => {
  return (
    <section className="bg-gray-300 py-16 md:py-24">
      <div className="container mx-auto px-6 md:px-12 flex flex-col lg:flex-row items-center justify-between">
        <div className="lg:w-1/2 lg:mr-12 mb-12 lg:mb-0">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-700 mb-4">
            More conversations,
            <br />
            <span className="text-slate-600">less outreach.</span>
          </h1>
          <h2 className="text-4xl md:text-5xl font-bold text-blue-600 mb-6">
            Bridger makes it easy.
          </h2>
        </div>
        <div className="lg:w-1/2">
          <div className="relative">
            <img
              src="/laptop-mockup.png" 
              alt="Video Call Application"
              className="w-full h-auto object-contain rounded-lg shadow-xl"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;