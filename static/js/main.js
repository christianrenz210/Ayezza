document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("lightboxModal");
  if (modal) {
    const titleEl = modal.querySelector("#lightboxLabel");
    const captionEl = modal.querySelector("#lightboxCaption");
    const imageEl = modal.querySelector("#lightboxImage");
    const downloadEl = modal.querySelector("#lightboxDownload");

    modal.addEventListener("show.bs.modal", function (event) {
      const card = event.relatedTarget;
      const title = card.getAttribute("data-title") || "Ayezza";
      const caption = card.getAttribute("data-caption") || "";
      const img = card.querySelector("img");
      const downloadLink = card.querySelector(".gallery-download");

      titleEl.textContent = title;
      captionEl.textContent = caption;
      if (img) {
        imageEl.src = img.src;
        imageEl.alt = title;
      }
      if (downloadLink) {
        downloadEl.href = downloadLink.href;
        downloadEl.setAttribute("download", downloadLink.getAttribute("download") || "");
      }
    });
  }

  const secret = document.getElementById("secretMessage");
  if (secret) {
    let lastY = window.scrollY;
    let revealed = false;

    window.addEventListener("scroll", function () {
      const y = window.scrollY;
      const scrollingDown = y > lastY;

      if (scrollingDown && y > 200 && !revealed) {
        secret.classList.add("show");
        revealed = true;
        setTimeout(function () {
          secret.classList.remove("show");
          revealed = false;
        }, 3500);
      } else if (!scrollingDown) {
        secret.classList.remove("show");
        revealed = false;
      }
      lastY = y;
    }, { passive: true });
  }

  const bgMusic = document.getElementById("bgMusic");
  const musicToggle = document.getElementById("musicToggle");
  const vinyl = document.getElementById("vinyl");
  if (bgMusic && musicToggle) {
    function toggleMusic() {
      if (bgMusic.paused) {
        bgMusic.play();
      } else {
        bgMusic.pause();
      }
    }
    musicToggle.addEventListener("click", toggleMusic);
    if (vinyl) {
      vinyl.addEventListener("click", toggleMusic);
      vinyl.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          toggleMusic();
        }
      });
    }
    bgMusic.addEventListener("play", function () {
      musicToggle.setAttribute("aria-pressed", "true");
      musicToggle.innerHTML = '<i class="bi bi-pause-fill" aria-hidden="true"></i> Pause';
      if (vinyl) vinyl.classList.add("spinning");
      if (lyricsView) {
        lyricsView.classList.add("revealed");
        vinylView.classList.remove("is-active");
        lyricsView.classList.add("is-active");
      }
      if (viewTabs && viewTabs.length) {
        viewTabs.forEach(function (t) {
          t.classList.toggle("is-active", t.dataset.view === "lyrics");
        });
      }
    });
    bgMusic.addEventListener("pause", function () {
      musicToggle.setAttribute("aria-pressed", "false");
      musicToggle.innerHTML = '<i class="bi bi-play-fill" aria-hidden="true"></i> Play';
      if (vinyl) vinyl.classList.remove("spinning");
    });
  }

  const vinylView = document.getElementById("vinylView");
  const lyricsView = document.getElementById("lyricsView");
  const viewTabs = document.querySelectorAll(".view-tab");
  if (vinylView && lyricsView && viewTabs.length) {
    viewTabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        const target = tab.dataset.view;
        const showVinyl = target === "vinyl";
        vinylView.classList.toggle("is-active", showVinyl);
        lyricsView.classList.toggle("is-active", !showVinyl);
        viewTabs.forEach(function (t) {
          t.classList.toggle("is-active", t === tab);
        });
      });
    });
  }

  const lyricsText = document.querySelector("#lyricsView .lyrics-text");
  const lyricsBox = document.querySelector("#lyricsView .lyrics-box");
  let lyricLines = [];
  let lineTexts = [];
  if (lyricsText) {
    lyricLines = Array.prototype.slice.call(lyricsText.querySelectorAll(".lyric-line"));
    lineTexts = lyricLines.map(function (el) { return el.textContent; });
    lyricsText.classList.add("lyrics-lines");
  }

  let typingTimer = null;
  let typedIndex = -1;

  function typeLine(idx) {
    if (typingTimer) { clearInterval(typingTimer); typingTimer = null; }
    const el = lyricLines[idx];
    const full = lineTexts[idx] || "";
    let i = 0;
    el.textContent = "";
    typingTimer = setInterval(function () {
      el.textContent = full.slice(0, i + 1);
      i++;
      if (i >= full.length) {
        clearInterval(typingTimer);
        typingTimer = null;
      }
    }, 35);
  }

  function updateLyrics() {
    if (!bgMusic || !lyricLines.length) return;
    const t = bgMusic.currentTime;
    const dur = bgMusic.duration;
    let idx;
    const maxTime = parseFloat(lyricLines[lyricLines.length - 1].dataset.time) || 0;

    if (isFinite(dur) && dur > 0 && dur < maxTime * 1.1) {
      idx = Math.floor((t / dur) * lyricLines.length);
    } else {
      idx = 0;
      for (let i = 0; i < lyricLines.length; i++) {
        if (t >= parseFloat(lyricLines[i].dataset.time)) idx = i;
      }
    }
    idx = Math.max(0, Math.min(idx, lyricLines.length - 1));
    if (lyricLines[idx] && !lyricLines[idx].classList.contains("active")) {
      console.log("[Leonora Lyrics] " + lineTexts[idx]);
    }
    lyricLines.forEach(function (el, i) {
      const isActive = i === idx;
      el.classList.toggle("active", isActive);
      el.classList.toggle("near", Math.abs(i - idx) === 1);
      if (!isActive && el.textContent !== lineTexts[i]) {
        el.textContent = lineTexts[i];
      }
    });
    if (idx !== typedIndex) {
      typedIndex = idx;
      typeLine(idx);
    }
    if (lyricsBox && lyricLines[idx]) {
      const target = lyricLines[idx];
      lyricsBox.scrollTop = target.offsetTop - lyricsBox.clientHeight / 2 + target.clientHeight / 2;
    }
  }

  if (bgMusic) {
    bgMusic.addEventListener("timeupdate", updateLyrics);
    bgMusic.addEventListener("loadedmetadata", updateLyrics);
  }

  if (lyricLines.length && typeof STATIC_BASE !== "undefined") {
    fetch(STATIC_BASE + "lyrics_timestamps.json")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (data && Array.isArray(data.times) && data.times.length === lyricLines.length) {
          data.times.forEach(function (tm, i) {
            lyricLines[i].dataset.time = String(tm);
          });
          updateLyrics();
        }
      })
      .catch(function () { /* ignore */ });
  }

  const catData = document.getElementById("catData");
  const foldersView = document.getElementById("foldersView");
  const contentView = document.getElementById("folderContentView");
  const folderGrid = document.getElementById("folderGrid");
  const folderTitle = document.getElementById("folderTitle");
  const backBtn = document.getElementById("backBtn");

  if (catData && foldersView && contentView && folderGrid) {
    const categories = JSON.parse(catData.textContent);

    function buildCard(img) {
      const fig = document.createElement("figure");
      fig.className = "gallery-card";
      fig.setAttribute("data-bs-toggle", "modal");
      fig.setAttribute("data-bs-target", "#lightboxModal");
      fig.setAttribute("data-title", img.title);
      fig.setAttribute("data-caption", img.caption);

      const frame = document.createElement("div");
      frame.className = "gallery-frame";

      const image = document.createElement("img");
      image.src = STATIC_BASE + img.img;
      image.alt = img.title;
      image.loading = "lazy";

      const badge = document.createElement("span");
      badge.className = "gallery-badge";
      badge.innerHTML = '<i class="bi bi-image" aria-hidden="true"></i>';

      const dl = document.createElement("a");
      dl.className = "gallery-download";
      dl.href = STATIC_BASE + img.img;
      dl.download = img.img.split("/").pop();
      dl.title = "Download image";
      dl.setAttribute("aria-label", "Download " + img.title);
      dl.innerHTML = '<i class="bi bi-download" aria-hidden="true"></i>';

      frame.appendChild(image);
      frame.appendChild(badge);
      frame.appendChild(dl);

      const cap = document.createElement("figcaption");
      cap.className = "gallery-caption";
      cap.innerHTML = '<span class="caption-title"></span><span class="caption-text"></span>';
      cap.querySelector(".caption-title").textContent = img.title;
      cap.querySelector(".caption-text").textContent = img.caption;

      fig.appendChild(frame);
      fig.appendChild(cap);
      return fig;
    }

    function openFolder(index) {
      const cat = categories[index];
      if (!cat) return;
      folderGrid.innerHTML = "";
      cat.images.forEach(function (img) {
        folderGrid.appendChild(buildCard(img));
      });
      folderTitle.textContent = cat.name;
      foldersView.hidden = true;
      contentView.hidden = false;
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    document.querySelectorAll(".folder-card").forEach(function (btn) {
      btn.addEventListener("click", function () {
        openFolder(parseInt(btn.dataset.index, 10));
      });
    });

    if (backBtn) {
      backBtn.addEventListener("click", function () {
        contentView.hidden = true;
        foldersView.hidden = false;
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    }
  }
});
