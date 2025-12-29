# Deployment Checklist

Use this checklist to ensure your deployment is successful.

## 📋 Pre-Deployment Checklist

### Local Testing
- [ ] Run `python download_model.py` - model downloads successfully
- [ ] Run `python app.py` - app starts without errors
- [ ] Upload test image - background removal works
- [ ] Test with transparent background
- [ ] Test with colored backgrounds
- [ ] Check file sizes are reasonable
- [ ] Test batch upload (multiple images)
- [ ] Verify all static files load correctly

### Code Quality
- [ ] No hardcoded secrets or API keys in code
- [ ] `.env` file not committed (in .gitignore)
- [ ] Large model files not committed (in .gitignore)
- [ ] All dependencies in `requirements.txt`
- [ ] No debug code or print statements left
- [ ] Error handling in place for model loading
- [ ] Proper file upload validation

### Git Repository
- [ ] All changes committed
- [ ] `.gitignore` properly configured
- [ ] `README.md` updated with instructions
- [ ] `DEPLOYMENT.md` available
- [ ] `.gitkeep` files in empty directories
- [ ] Repository pushed to GitHub

## 🚀 Render.com Deployment

### Setup on Render
- [ ] Account created at render.com
- [ ] GitHub account connected
- [ ] Repository selected for deployment

### Configuration
- [ ] `render.yaml` exists in repository
- [ ] Build command includes model download
- [ ] Start command uses gunicorn
- [ ] Environment variables configured:
  - [ ] `PYTHON_VERSION` = 3.11.0
  - [ ] `SECRET_KEY` = (auto-generated or custom)
  - [ ] `DEBUG` = False
  - [ ] `FLASK_ENV` = production

### Monitoring Deployment
- [ ] Watch build logs in Render dashboard
- [ ] Verify model download completes (~168MB)
- [ ] Check for any build errors
- [ ] Wait for "Deploy successful" message
- [ ] Note your app URL: `https://your-app.onrender.com`

### Post-Deployment Testing
- [ ] Access app URL in browser
- [ ] Homepage loads correctly
- [ ] Upload single image works
- [ ] Background removal successful
- [ ] Different background colors work
- [ ] Batch upload works
- [ ] Gallery page loads
- [ ] Download processed images
- [ ] No console errors in browser dev tools
- [ ] Response times acceptable (expect slower on free tier)

## 🔧 Troubleshooting Checklist

If deployment fails, check:

### Build Errors
- [ ] Python version correct in `runtime.txt`
- [ ] All dependencies install successfully
- [ ] Model download completes (check logs)
- [ ] No missing files or imports
- [ ] File paths are correct (Linux paths on server)

### Runtime Errors
- [ ] App starts and binds to `$PORT`
- [ ] Gunicorn command correct
- [ ] No import errors
- [ ] Model file exists after build
- [ ] Static files accessible

### Performance Issues
- [ ] Reduce workers if memory errors
- [ ] Increase timeout if needed
- [ ] Consider upgrading plan for better performance
- [ ] Optimize image sizes before processing

### File Upload Issues
- [ ] Disk storage mounted correctly
- [ ] Upload folder writable
- [ ] File size limits appropriate
- [ ] Proper file type validation

## ✅ Success Criteria

Your deployment is successful when:

1. ✅ Build completes without errors
2. ✅ App starts and responds to health checks
3. ✅ Homepage loads with all styles
4. ✅ Can upload and process images
5. ✅ Background removal works correctly
6. ✅ Can download processed images
7. ✅ No errors in Render logs
8. ✅ Response times acceptable for your use case

## 📊 Performance Expectations

### Free Tier
- First request after inactivity: 30-60 seconds (cold start)
- Subsequent requests: 2-5 seconds per image
- Max file size: 16MB recommended
- Concurrent requests: Limited

### Paid Tier (Starter+)
- No cold starts with persistent instances
- Faster processing: 1-3 seconds per image
- Better for production use
- More memory for larger images

## 🔄 Continuous Deployment

Once set up:
- [ ] Push changes to GitHub main branch
- [ ] Render automatically rebuilds
- [ ] New version deployed (2-5 minutes)
- [ ] No manual steps needed

## 📝 Environment Variables Reference

| Variable | Local Dev | Render.com | Required |
|----------|-----------|------------|----------|
| SECRET_KEY | From .env | Auto-generated | Yes |
| DEBUG | True | False | Yes |
| FLASK_ENV | development | production | Yes |
| PYTHON_VERSION | (N/A) | 3.11.0 | Yes |
| PORT | 5000 | Auto-set | No |

## 🆘 Getting Help

If issues persist:
1. Check Render logs: Dashboard → Logs tab
2. Review `DEPLOYMENT.md` troubleshooting section
3. Check Render status: status.render.com
4. Verify build output line by line
5. Test locally to isolate issues

## 🎉 Post-Deployment

After successful deployment:
- [ ] Share app URL with team/users
- [ ] Monitor usage and performance
- [ ] Set up custom domain (optional)
- [ ] Configure auto-scaling if needed
- [ ] Set up monitoring/alerts
- [ ] Document any custom configurations

---

**Remember**: The model file is automatically downloaded during deployment - you don't need to commit it to Git!
