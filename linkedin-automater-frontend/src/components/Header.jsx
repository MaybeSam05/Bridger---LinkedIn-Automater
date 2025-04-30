import React from "react";

const banner = "py-4 px-6 md:px-12 relative flex items-center justify-between";
const img = "object-contain";

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

    </header>
  );
};

export default Header;