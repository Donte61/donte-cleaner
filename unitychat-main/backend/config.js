const config = {
    server: 'DESKTOP-64ESNB3',  // Tam sunucu adı ve instance
    database: 'ChatApp',
    user: 'chatapp_user',
    password: 'ChatApp123!',
    options: {
        encrypt: false,
        trustServerCertificate: true,
        enableArithAbort: true,
        port: 1433,
        connectTimeout: 30000,
        requestTimeout: 30000
    }
};

module.exports = config;
