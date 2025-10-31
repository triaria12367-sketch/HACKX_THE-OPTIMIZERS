// backend/server.js
const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const RECORDINGS_DIR = path.join(__dirname, '../recordings');

// Ensure recordings folder exists
if (!fs.existsSync(RECORDINGS_DIR)) {
  fs.mkdirSync(RECORDINGS_DIR);
}

app.use(express.static(path.join(__dirname, 'public')));

// Store active recordings: socket.id → writeStream
const activeRecordings = new Map();

io.on('connection', (socket) => {
  console.log('User connected:', socket.id);

  // New recording starts
  socket.on('start-recording', () => {
    const filename = `recording_${socket.id}_${Date.now()}.webm`;
    const filepath = path.join(RECORDINGS_DIR, filename);
    const writeStream = fs.createWriteStream(filepath);

    activeRecordings.set(socket.id, { stream: writeStream, filename });
    console.log(`Recording started: ${filename}`);
  });

  // Receive video chunk
  socket.on('video-chunk', (chunk) => {
    const recording = activeRecordings.get(socket.id);
    if (recording) {
      recording.stream.write(chunk);
    }

    // Broadcast to others
    socket.broadcast.emit('live-video-chunk', chunk);
  });

  // Stop recording
  socket.on('stop-recording', () => {
    const recording = activeRecordings.get(socket.id);
    if (recording) {
      recording.stream.end();
      activeRecordings.delete(socket.id);
      console.log(`Recording saved: ${recording.filename}`);
      
      // Notify all clients
      io.emit('recording-saved', {
        filename: recording.filename,
        url: `/recordings/${recording.filename}`
      });
    }
  });

  socket.on('disconnect', () => {
    // Auto-stop if disconnected
    const recording = activeRecordings.get(socket.id);
    if (recording) {
      recording.stream.end();
      activeRecordings.delete(socket.id);
      console.log(`Recording auto-saved on disconnect: ${recording.filename}`);
    }
    console.log('User disconnected:', socket.id);
  });
});

server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});