import React from "react";
import { Link } from "react-router-dom";

const banner = "py-4 px-6 md:px-12 relative flex items-center justify-between";
const img = "object-contain";

const Header = () => {
  return (
    <header className={banner}>
      <div className="flex items-center z-10">
        <Link to="/">
        <img
          src="/finaldesignBG.png"
          alt="Bridger Logo"
          className={img}
          style={{ height: "55px", width: "auto" }}
        />
        </Link>
      </div>

    </header>
  );
};

export default Header;