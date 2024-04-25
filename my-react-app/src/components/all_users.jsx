import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AllUsers = () => {
    const [users, setUsers] = useState([]);

    const getUsers = async () => {
        try {
            const token = localStorage.getItem('token'); // Get the token from local storage
            const response = await axios.get('http://localhost:8000/users', {
                headers: {
                    Authorization: `Bearer ${token}` // Include the token in the Authorization header
                }
            });
            setUsers(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        getUsers();
    }, []);

    return (
        <div>
            <button onClick={getUsers}>Get All Users</button>
            <ul>
                {users.map((user) => (
                    <li key={user.id}>{user.id}</li>
                ))}
            </ul>
        </div>
    );
};

export default AllUsers;