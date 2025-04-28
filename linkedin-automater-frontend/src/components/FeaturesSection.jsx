import React from "react";
import { Link, Pencil, Check } from "lucide-react";

const FeaturesSection = () => {
  const features = [
    {
      icon: <Link size={40} className="text-blue-600" style = {{ color: "#2C3E50"}}/>,
      title: "Find your Connection",
      description: "Paste your desired LinkedIn Profile",
    },
    {
      icon: <Pencil size={40} className="text-blue-600" style = {{ color: "#2C3E50"}}/>,
      title: "Customize your Message",
      description: "Bridger drafts the email based on similarities",
    },
    {
      icon: <Check size={55} className="text-blue-600" style = {{ color: "#2C3E50"}}/>,
      title: "Send Automatically",
      description: "Bridger sends it for you, effortlessly.",
    },
  ];

  return (
    <section className="py-16 px-6 md:px-12">
      <div className="container mx-auto">
        <div className="grid md:grid-cols-3 gap-12">
          {features.map((feature, index) => (
            <div key={index} className="flex flex-col items-center text-center">
              <div className="w-24 h-24 rounded-full border-4 border-blue-600 flex items-center justify-center mb-6" style = {{ borderColor: "#2C3E50"}}>
                {feature.icon}
              </div>
              <h3 className="text-2xl font-bold mb-3 text-slate-800">{feature.title}</h3>
              <p className="text-slate-600 font-bold text-lg">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
