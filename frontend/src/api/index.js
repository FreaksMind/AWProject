import axios from 'axios'
const API_URL = 'http://localhost:5000/'

export function login (userData) {
  axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
  return axios.post(`${API_URL}/login`, { params: {
      email: userData.email,
      password: userData.password
    }
  }, ) 
};

export function register (userData) {
  return axios.post(`${API_URL}/register`, { params: {
    nume: userData.nume,
    prenume: userData.prenume,
    email: userData.email,
    telefon: userData.phone_number,
    password: userData.password,
    isDoctor: userData.isDoctor
    }
  }) 
};

export async function download_ontology() {
  const apiData = await axios.get(`${API_URL}/download_ontology`);
  return apiData.data;
};

export async function generate_ontology(){
  await axios.post(`${API_URL}/generate_ontology`);
}

export async function get_user_details (userData) {
  const apiData = await axios.get(`${API_URL}/user/details`, { 
    params: {
      email: userData.email
    }
  });

  return apiData.data;
};

export async function generate_reset_code (userData) {
  const apiData = await axios.post(`${API_URL}/password/generate/reset`, { 
    params: {
      email: userData.email,
    }
  });

  return apiData.data;
};

export async function get_reset_info (data) {

  const apiData = await axios.get(`${API_URL}/reset/get`, { 
    params: {
      reset_code: data.reset_code,
    }
  });

  return apiData.data;
};


export async function update_password (userData) {
  const apiData = await axios.post(`${API_URL}/password/update/`, { 
    params: {
      password: userData.password,
      user_id: userData.user_id
    }
  });

  return apiData.data;
};

export async function confirm_account (userData) {
  const apiData = await axios.post(`${API_URL}/confirm/`, { 
    params: {
      confirmation_code: userData.confirmation_code
    }
  });

  return apiData.data;
};
