# Project Roadmap and TODO

## Completed ✓

- [x] Set up project structure
- [x] Create source code modules (detection, tracking, counting)
- [x] Add configuration system
- [x] Write comprehensive documentation
- [x] Add .gitignore for Python projects
- [x] Create requirements.txt with dependencies
- [x] Add example notebook
- [x] Create basic test suite
- [x] Set up data and models directories

## Next Steps

### Phase 1: Data Collection and Preparation
- [ ] Collect video data from fish migration sites
- [ ] Organize videos in `data/raw/` directory
- [ ] Document video metadata (location, date, time, conditions)
- [ ] Create sample dataset for initial testing

### Phase 2: Model Training
- [ ] Annotate fish in video frames (use LabelImg or CVAT)
- [ ] Save annotations in YOLO format in `data/annotations/`
- [ ] Split data into train/val/test sets
- [ ] Train YOLOv8 model on annotated data
- [ ] Evaluate model performance (mAP, precision, recall)
- [ ] Save trained model to `models/` directory
- [ ] Update `config/config.yaml` with model path

### Phase 3: System Validation
- [ ] Process test videos with trained model
- [ ] Manually count fish in test videos for validation
- [ ] Compare automated counts with manual counts
- [ ] Calculate accuracy metrics
- [ ] Document validation results

### Phase 4: Parameter Optimization
- [ ] Fine-tune detection confidence threshold
- [ ] Optimize tracking parameters (max_distance, max_disappeared)
- [ ] Adjust counting line position for different videos
- [ ] Test different frame skip rates for performance
- [ ] Document optimal settings for different scenarios

### Phase 5: Batch Processing
- [ ] Create scripts for processing multiple videos
- [ ] Set up batch processing workflow
- [ ] Process entire dataset
- [ ] Aggregate statistics across all videos
- [ ] Generate summary reports

### Phase 6: Analysis and Reporting
- [ ] Create analysis notebooks for data exploration
- [ ] Generate visualizations (charts, graphs, heatmaps)
- [ ] Analyze migration patterns over time
- [ ] Compare different locations/conditions
- [ ] Write final project report

### Phase 7: Improvements and Extensions (Optional)
- [ ] Add species classification (if multiple species present)
- [ ] Implement size estimation for individual fish
- [ ] Add behavior analysis (schooling patterns, feeding)
- [ ] Create web dashboard for monitoring
- [ ] Add real-time streaming video support
- [ ] Implement database for long-term data storage

## Current Priorities

1. **Collect video data** - Need sample videos to test the system
2. **Annotate training data** - At least 100-200 annotated frames needed
3. **Train initial model** - Even a small model will be better than placeholder
4. **Validate on test video** - Ensure system works end-to-end

## Technical Debt

- [ ] Add more comprehensive unit tests
- [ ] Add integration tests
- [ ] Add input validation for configuration
- [ ] Improve error handling throughout
- [ ] Add logging system for debugging
- [ ] Add progress bars for long-running operations
- [ ] Optimize video processing for better performance
- [ ] Add support for more video formats

## Documentation Needed

- [ ] Tutorial for annotation workflow
- [ ] Model training guide with step-by-step instructions
- [ ] Troubleshooting guide with common issues
- [ ] API documentation for each module
- [ ] Performance benchmarking results
- [ ] Validation methodology documentation

## Team Assignments

Suggested task distribution (adjust based on team size and skills):

**Person 1 - Data Collection & Annotation**:
- Collect videos
- Annotate training data
- Manage data organization

**Person 2 - Model Training & Optimization**:
- Train detection models
- Optimize parameters
- Validate results

**Person 3 - System Integration & Testing**:
- Test full pipeline
- Fix bugs
- Improve performance

**Person 4 - Analysis & Reporting**:
- Process datasets
- Analyze results
- Create visualizations
- Write reports

## Resources

### Annotation Tools
- LabelImg: https://github.com/tzutalin/labelImg
- CVAT: https://github.com/openvinotoolkit/cvat
- Label Studio: https://labelstud.io/

### Model Training
- Ultralytics YOLOv8: https://docs.ultralytics.com/
- YOLO Tutorial: https://docs.ultralytics.com/modes/train/

### Sample Datasets (for reference)
- Check for publicly available fish datasets
- Consult with advisor for existing data

## Timeline Suggestions

**Weeks 1-2**: Data collection and project setup  
**Weeks 3-4**: Data annotation and model training  
**Weeks 5-6**: System validation and optimization  
**Weeks 7-8**: Batch processing and analysis  
**Weeks 9-10**: Report writing and presentation prep  

## Notes

- Keep regular backups of data and models
- Document all decisions and parameters used
- Version control configurations that work well
- Regular team meetings to discuss progress
- Consider ethical implications of monitoring wildlife

## Questions to Address

- What is the target accuracy for the system?
- How many videos need to be processed?
- What time period does the data cover?
- Are there multiple locations/sites?
- Will the system be used for future monitoring?
- What format should final deliverables be in?

---

**Last Updated**: [Current Date]  
**Next Review**: Check weekly during team meetings
