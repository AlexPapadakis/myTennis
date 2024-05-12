import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CURRENT_ATHLETE_API_URL, CURRENT_USER_API_URL } from '../../constants';

function EditableField({label, initialValue ,className,fieldName, type, options}) {
    const [value, setValue] = useState(initialValue);
    const [isEditing, setIsEditing] = useState(false);


    useEffect(() => {
        setValue(initialValue);
    }, [initialValue]);

    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleAbortClick = () => {
        setIsEditing(false);
        setValue(initialValue);
    };

    const handleSaveClick = () => {
        

        if (className === "user") {
            axios.put(CURRENT_USER_API_URL, {
                [fieldName]: value
            }, {
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.log(error);
            });
        } else {
            axios.put(CURRENT_ATHLETE_API_URL, {
                [fieldName]: value
            }, {
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.log(error);
            });
        }
        setIsEditing(false);
    };

 
    const renderInput = () => {
        switch(type) {
            case 'text':
                return <input type="text" value={value} onChange={e => setValue(e.target.value)} />;
            case 'select':
                return (
                    <select value={value} onChange={e => setValue(e.target.value)}>
                        {options.map(option => (
                            <option key={option} value={option}>{option}</option>
                        ))}
                    </select>
                );
            case 'date':
                return <input type="date" value={value} onChange={e => setValue(e.target.value)} />;
            default:
                return <input type="text" value={value} onChange={e => setValue(e.target.value)} />;
        }
    };
    return (
        <div>
            {isEditing ? (
                <div>
                    <label>
                        {label}
                    </label>
                    {renderInput()}
                    <button onClick={handleAbortClick}>X</button>
                    <button onClick={handleSaveClick}>Save</button>
                </div>
            ) : (
                <div>
                    <label>
                        {label}
                    </label>
                    <p> {value} </p>
                    <button onClick={handleEditClick}>Edit</button>
                </div>
            )}
        </div>
    );
}

export default EditableField;