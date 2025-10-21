import { useEffect, useState } from "react";
import { authService, User } from "../services/auth";
import { User as UserIcon, Mail, LogOut, Shield } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const UserProfile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUserInfo();
  }, []);

  const loadUserInfo = async () => {
    try {
      const userInfo = await authService.fetchUserInfo();
      setUser(userInfo);
    } catch (error) {
      console.error("Failed to load user info:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    navigate("/login");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">User Profile</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your account information
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-8">
            <div className="flex items-center">
              <div className="bg-white rounded-full p-4">
                <UserIcon className="w-12 h-12 text-blue-600" />
              </div>
              <div className="ml-6 text-white">
                <h2 className="text-2xl font-bold">{user?.username}</h2>
                <p className="text-blue-100 mt-1">Active User</p>
              </div>
            </div>
          </div>

          <div className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-start">
                <UserIcon className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">Username</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {user?.username}
                  </p>
                </div>
              </div>

              <div className="flex items-start">
                <Shield className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-gray-500">User ID</p>
                  <p className="text-lg font-mono text-gray-900">
                    {user?.user_id}
                  </p>
                </div>
              </div>

              {user?.email && (
                <div className="flex items-start">
                  <Mail className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-500">Email</p>
                    <p className="text-lg text-gray-900">{user.email}</p>
                  </div>
                </div>
              )}
            </div>

            <div className="pt-6 border-t">
              <button
                onClick={handleLogout}
                className="flex items-center px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5 mr-2" />
                Sign Out
              </button>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Session Information
          </h3>
          <p className="text-sm text-blue-700">
            Your session will expire after 30 minutes of inactivity. You'll be
            automatically redirected to the login page.
          </p>
        </div>
      </div>
    </div>
  );
};
