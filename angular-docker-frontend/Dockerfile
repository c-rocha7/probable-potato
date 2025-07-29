# Dockerfile para aplicação Angular
FROM node:22.17.1-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY package*.json ./

# Instala as dependências (incluindo devDependencies para ter o Angular CLI)
RUN npm ci

# Copia o código fonte
COPY . .

# Expõe a porta 4200 (padrão do Angular)
EXPOSE 4200

# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "start:docker"]
