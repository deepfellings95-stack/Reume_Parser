import React from "react";
import { Link } from "react-router-dom";

const BaseLayout = ({
  children,
  setIsSignupOpen,
  setIsLoginOpen,
  isAuthenticated,
}) => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* NAVBAR */}
      <nav className="fixed top-0 left-0 w-full z-50 bg-gray-900 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <img
              src="https://flowbite.com/docs/images/logo.svg"
              alt="Logo"
              className="h-8"
            />
            <span className="text-white text-xl font-bold">
              Ace Your Resume
            </span>
          </Link>

          {/* Nav Links */}
          <ul className="hidden md:flex items-center gap-6 text-gray-300">
            <li>
              <Link to="/" className="hover:text-white transition">
                Home
              </Link>
            </li>
            <li>
              <Link to="/about" className="hover:text-white transition">
                About
              </Link>
            </li>
            <li>
              <Link to="/pricing" className="hover:text-white transition">
                Pricing
              </Link>
            </li>
            <li>
              <Link to="/contact" className="hover:text-white transition">
                Contact
              </Link>
            </li>
          </ul>

          {/* Auth Buttons */}
          <div className="flex items-center gap-3">
            {!isAuthenticated ? (
              <>
                <button
                  onClick={() => setIsLoginOpen(true)}
                  className="text-gray-300 hover:text-white transition"
                >
                  Login
                </button>
                <button
                  onClick={() => setIsSignupOpen(true)}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition"
                >
                  Sign Up
                </button>
              </>
            ) : (
              <span className="text-green-400 font-medium">
                Logged In
              </span>
            )}
          </div>
        </div>
      </nav>

      {/* PAGE CONTENT */}
      <main className=" flex-grow bg-neutral-secondary-soft">
        {children}
      </main>

      {/* FOOTER */}
      <footer className="bg-gray-900 text-gray-400 text-center py-4 text-sm">
        © {new Date().getFullYear()} Ace Your Resume. All rights reserved.
      </footer>
    </div>
  );
};

export default BaseLayout;
