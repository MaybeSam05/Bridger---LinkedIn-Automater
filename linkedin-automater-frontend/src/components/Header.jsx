import React from "react";

const banner = "py-4 px-6 md:px-12 relative flex items-center justify-between";
const img = "object-contain";
const title = "absolute left-1/2 transform -translate-x-1/2 md:text-3xl font-bold text-lg font-medium";

const Header = () => {
  return (
    <header className={banner}>
      {/* Logo on the left */}
      <div className="flex items-center z-10">
        <img
          src="/finaldesignBG.png"
          alt="Bridger Logo"
          className={img}
          style={{ height: "55px", width: "auto" }}
        />
      </div>

      {/* Centered Title */}
      <h2 className={title} style={{ color: "#000000" }}>
        LinkedIn Connect Tool
      </h2>
    </header>
  );
};

export default Header;