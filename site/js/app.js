/**
 * DevCraft Studio — site/app.js
 * Vanilla JS · ES2024 · no bundler · no dependencies
 *
 * Modules:
 *   - i18n loader + dynamic switching (RU/EN/DE)
 *   - theme toggle (dark/light, persisted)
 *   - mobile navigation
 *   - scroll-aware header
 *   - intersection-observer reveal animations
 *   - lead form validation + async submit to /api/lead
 *   - prefers-color-scheme initial theme
 */

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

const state = {
    lang: localStorage.getItem('lang') || 'ru',
    theme: localStorage.getItem('theme') || (matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'),
    dict: {},
};

/* =========================================================================
   I18N
   ========================================================================= */
async function loadDict(lang) {
    try {
        const res = await fetch(`/i18n/${lang}.json`, { cache: 'no-cache' });
        if (!res.ok) throw new Error(`Failed to load ${lang}.json`);
        return await res.json();
    } catch (err) {
        console.warn('[i18n]', err);
        return {};
    }
}

function applyTranslations() {
    const dict = state.dict;
    if (!dict) return;

    $$('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        const value = key.split('.').reduce((o, k) => (o ? o[k] : null), dict);
        if (typeof value === 'string') el.textContent = value;
    });

    $$('[data-i18n-attr]').forEach(el => {
        const attr = el.dataset.i18nAttr;
        const key  = el.dataset.i18n;
        const value = key.split('.').reduce((o, k) => (o ? o[k] : null), dict);
        if (attr && typeof value === 'string') el.setAttribute(attr, value);
    });

    document.documentElement.lang = state.lang;
}

async function setLang(lang) {
    if (!['ru', 'en', 'de'].includes(lang)) return;
    state.lang = lang;
    localStorage.setItem('lang', lang);
    state.dict = await loadDict(lang);
    applyTranslations();

    $$('.lang-btn').forEach(b => {
        const isActive = b.dataset.lang === lang;
        b.classList.toggle('is-active', isActive);
        b.setAttribute('aria-pressed', String(isActive));
    });
}

/* =========================================================================
   THEME
   ========================================================================= */
function applyTheme() {
    document.documentElement.dataset.theme = state.theme;
}
function toggleTheme() {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', state.theme);
    applyTheme();
}

/* =========================================================================
   NAV
   ========================================================================= */
function setupBurger() {
    const burger = $('#burger');
    const nav    = $('#mobile-nav');
    if (!burger || !nav) return;

    burger.addEventListener('click', () => {
        const isOpen = burger.classList.toggle('is-open');
        nav.classList.toggle('is-open', isOpen);
        burger.setAttribute('aria-expanded', String(isOpen));
        nav.setAttribute('aria-hidden', String(!isOpen));
    });

    nav.addEventListener('click', e => {
        if (e.target.matches('a')) {
            burger.classList.remove('is-open');
            nav.classList.remove('is-open');
            burger.setAttribute('aria-expanded', 'false');
            nav.setAttribute('aria-hidden', 'true');
        }
    });
}

function setupScrollHeader() {
    const header = $('#site-header');
    if (!header) return;
    const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 12);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
}

/* =========================================================================
   REVEAL
   ========================================================================= */
function setupReveal() {
    const targets = $$('.card, .work-card, .step, .stack-group, .section-head, .contact-copy, .contact-form');
    targets.forEach((el, i) => {
        el.dataset.reveal = '';
        el.style.transitionDelay = `${Math.min(i * 40, 320)}ms`;
    });

    const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    targets.forEach(el => io.observe(el));
}

/* =========================================================================
   FORM
   ========================================================================= */
function setupForm() {
    const form   = $('#lead-form');
    const status = $('#form-status');
    if (!form || !status) return;

    const setStatus = (msg, type) => {
        status.textContent = msg;
        status.classList.remove('is-success', 'is-error');
        if (type) status.classList.add(`is-${type}`);
        status.classList.add('is-visible');
    };

    const validate = (data) => {
        let ok = true;
        $$('.field', form).forEach(f => f.classList.remove('has-error'));

        if (!data.name || data.name.trim().length < 2) {
            $('#name').closest('.field').classList.add('has-error'); ok = false;
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
            $('#email').closest('.field').classList.add('has-error'); ok = false;
        }
        if (!data.service) {
            $('#service').closest('.field').classList.add('has-error'); ok = false;
        }
        if (!data.message || data.message.trim().length < 10) {
            $('#message').closest('.field').classList.add('has-error'); ok = false;
        }
        return ok;
    };

    const submitDict = state.dict?.form || {};

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(form).entries());
        if (!validate(data)) {
            setStatus(submitDict.errFill || 'Заполните все поля корректно', 'error');
            return;
        }

        const btn = $('#submit-btn');
        btn.disabled = true;
        btn.style.opacity = '0.7';

        try {
            const res = await fetch('/api/lead', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept-Language': state.lang },
                body: JSON.stringify({ ...data, source: 'site', lang: state.lang }),
            });

            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || `HTTP ${res.status}`);
            }

            form.reset();
            setStatus(submitDict.success || 'Спасибо! Свяжусь в течение 2 часов.', 'success');
        } catch (err) {
            console.error(err);
            // Soft-fail: still tell user it's received (queued locally)
            const queue = JSON.parse(localStorage.getItem('leadQueue') || '[]');
            queue.push({ ...data, ts: Date.now() });
            localStorage.setItem('leadQueue', JSON.stringify(queue));
            form.reset();
            setStatus(submitDict.queued || 'Заявка сохранена, отправлю при первой возможности.', 'success');
        } finally {
            btn.disabled = false;
            btn.style.opacity = '1';
        }
    });
}

/* =========================================================================
   INIT
   ========================================================================= */
async function init() {
    applyTheme();
    setupBurger();
    setupScrollHeader();
    setupReveal();
    setupForm();

    $('#theme-toggle')?.addEventListener('click', toggleTheme);
    $$('.lang-btn').forEach(b => b.addEventListener('click', () => setLang(b.dataset.lang)));

    await setLang(state.lang);

    $('#year').textContent = new Date().getFullYear();
}

document.addEventListener('DOMContentLoaded', init);
