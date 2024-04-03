// import React, { useState } from 'react';
// import axios from 'axios';

// function LoginForm() {
//   const [formData, setFormData] = useState({
//     email: '',
//     password: '',
//   });

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await axios.post('/api/login', formData);
//       console.log(response.data);
//       // Handle success (e.g., store token, redirect to dashboard, etc.)
//     } catch (error) {
//       console.error(error);
//       // Handle error (e.g., show error message)
//     }
//   };

//   return (
//     <div className="container mx-auto p-4">
//       <form onSubmit={handleSubmit} className="space-y-4">
//         <div>
//           <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
//           <input
//             type="email"
//             name="email"
//             id="email"
//             value={formData.email}
//             onChange={handleChange}
//             className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
//             required
//           />
//         </div>
//         <div>
//           <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
//           <input
//             type="password"
//             name="password"
//             id="password"
//             value={formData.password}
//             onChange={handleChange}
//             className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
//             required
//           />
//         </div>
//         <div>
//           <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600">Login</button>
//         </div>
//       </form>
//     </div>
//   );
// }

// export default LoginForm;