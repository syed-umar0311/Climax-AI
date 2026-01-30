import { useState } from "react";
import Layout from "./Layout/Layout";
import AuthModal from "./Pages/AuthModal";

export default function App() {
  const [isUser, setIsUser] = useState(false);

  return (
    <>
      {!isUser ? (
        <AuthModal setIsUser={setIsUser} />
      ) : (
        <div className="bg-gray-50">
          <Layout />
        </div>
      )}
    </>
  );
}
