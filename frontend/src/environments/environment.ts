
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'pharrukh.eu', // the auth0 domain prefix
    audience: 'CoffeeAPI', // the audience set for the auth0 app
    clientId: '48pkDsZI9KbCbEEcGYJ4WmXChiDqVEPD', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application. 
  }
};
