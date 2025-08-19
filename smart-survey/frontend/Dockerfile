FROM node:20

WORKDIR /app
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of frontend code
COPY . .

EXPOSE 19000 19001 19002

# Start Expo in tunnel mode
CMD ["npx", "expo", "start", "--tunnel", "--non-interactive"]
