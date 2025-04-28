import React from "react";
import { Link, Pencil, Check } from "lucide-react";

const FeaturesSection = () => {
  const features = [
    {
      icon: <Link size={36} className="text-blue-600" />,
      title: "Find your Connection",
      description: "Paste your desired LinkedIn Profile",
    },
    {
      icon: <Pencil size={36} className="text-blue-600" />,
      title: "Customize your Message",
      description: "Bridger drafts the email based on similarities",
    },
    {
      icon: <Check size={36} className="text-blue-600" />,
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
              <div className="w-24 h-24 rounded-full border-2 border-blue-600 flex items-center justify-center mb-6">
                {feature.icon}
              </div>
              <h3 className="text-2xl font-bold mb-3 text-slate-800">{feature.title}</h3>
              <p className="text-slate-600 text-lg">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
