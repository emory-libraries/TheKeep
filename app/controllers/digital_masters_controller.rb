class DigitalMastersController < ApplicationController
  def index
    @content_pages = Paginator.new self, Content.count, 25, @params['page']
    @contents = Content.find_by_image_note('Dawson Grant')
    
    render :action => 'list'
  end

  # GETs should be safe (see http://www.w3.org/2001/tag/doc/whenToUseGet.html)
  verify :method => :post, :only => [ :destroy, :create, :update ],
         :redirect_to => { :action => :list }

  def list
    @content_pages, @contents = paginate :contents, :per_page => 10
  end

  def show
    @content = Content.find(params[:id])
  end

  def new
    @content = Content.new
  end

  def create
    @content = Content.new(params[:content])
    if @content.save
      flash[:notice] = 'Content was successfully created.'
      redirect_to :action => 'list'
    else
      render :action => 'new'
    end
  end
 
  def edit
    @content = Content.find(params[:id])
    #@src_still_image = @content.src_still_image
  end

  def update
    @content = Content.find(params[:id])
    if @content.update_attributes(params[:content])
      flash[:notice] = 'Content was successfully updated.'
      redirect_to :action => 'show', :id => @content
    else
      render :action => 'edit'
    end
  end

  def destroy
    Content.find(params[:id]).destroy
    redirect_to :action => 'list'
  end
  
  
#############################################################################
# Contents Names
#############################################################################
  def showContentNames
    @content = Content.find(params[:id])
    
    render :partial => 'content_name_table'
  end  
  
  def addContentName
  
    @nc = ContentsNames.new
    @nc.content_id = params[:content_id]
    
    #display pop_up edit window loaded with partial name_form next action saveContentName
    render :partial => "popup_edit", :locals => {:partial_name => "name_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentName', :id => @nc}}}    
    
  end 
  
  def editContentName
  
    @nc = ContentsNames.find(params[:id])
    @n = Name.find(@nc.name_id)
    @r = Role.find(@nc.role_id)
    
    #display pop_up edit window loaded with partial name_form next action saveContentName
    render :partial => "popup_edit", :locals => {:partial_name => "name_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentName', :id => @nc}}}    
    
  end 
 
  def saveContentName
    
    unless params[:id]
      nc = ContentsNames.new
    else
      nc = ContentsNames.find(params[:id])
    end
      
    #update with new values  
    nc.content_id = params[:nc][:content_id]
    nc.name_id = params[:nc][:name_id]
    nc.role_id = params[:nc][:role_id]
    nc.role_term = params[:nc][:role_term]
      
    nc.save
    
    @content = Content.find(nc.content_id)    
    render :partial => 'content_name_table'
  end  
  
#############################################################################
# Contents Subjects
#############################################################################
  def showContentSubjects
    @content = Content.find(params[:id])
    
    render :partial => 'content_subjects_table'
  end  
  
  def addContentSubject
  
    @cs = ContentsSubjects.new
    @cs.content_id = params[:content_id]
    
    #display pop_up edit window loaded with partial subjects_form next action saveContentSubject
    render :partial => "popup_edit", :locals => {:partial_name => "subject_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentSubject', :id => @cs}}}    
    
  end 
  
  def editContentSubject
  
    @cs = ContentsSubjects.find(params[:id])
    
    #display pop_up edit window loaded with partial subjects_form next action saveContentName
    render :partial => "popup_edit", :locals => {:partial_name => "subject_form", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveContentSubject', :id => @cs}}}    
    
  end 
 
  def saveContentSubject
    
    unless params[:id]
      cs = ContentsSubjects.new
    else
      cs = ContentsSubjects.find(params[:id])
    end
      
    #update with new values  
    cs.content_id = params[:cs][:content_id]
    cs.subject_id = params[:cs][:subject_id]
    cs.fieldnames = params[:cs][:fieldnames]

      
    cs.save
    
    @content = Content.find(cs.content_id)    
    render :partial => 'content_subjects_table'
  end  
  
#############################################################################
# Still Images
#############################################################################  
  def addSrcStillImage

      @srcStillImage = SrcStillImage.new
      @srcStillImage.content_id = params[:content_id]
      @content = Content.find(params[:content_id])
      
      render :partial => "popup_edit", :locals => {:partial_name => "still_img_subform", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveSrcStillImage', :id => @srcStillImage}}}    
  end
  
  def editSrcStillImage
    @srcStillImage = SrcStillImage.find(params[:id])
    render :partial => "popup_edit", :locals => {:partial_name => "still_img_subform", :action => {:complete => 'eval(request.responseText)', :url => { :action => 'saveSrcStillImage', :id => @srcStillImage}}}    
  end
  
  def saveSrcStillImage
    unless params[:id]
      srcStillImage = SrcStillImage.new
      @content = Content.find(params[:srcStillImage][:content_id])
    else
      srcStillImage = SrcStillImage.find(params[:id])
      @content = Content.find(srcStillImage.content_id)
    end    
    
    srcStillImage.form_id = params[:srcStillImage][:form_id]
    srcStillImage.dimension_height = params[:srcStillImage][:dimension_height]
    srcStillImage.dimension_height_unit = params[:srcStillImage][:dimension_height_unit]
    srcStillImage.dimension_width = params[:srcStillImage][:dimension_width]
    srcStillImage.dimension_width_unit = params[:srcStillImage][:dimension_width_unit]    
    srcStillImage.dimension_note = params[:srcStillImage][:dimension_note]
    srcStillImage.disposition = params[:srcStillImage][:disposition]
    srcStillImage.generation = params[:srcStillImage][:generation]
    srcStillImage.source_note = params[:srcStillImage][:source_note]
    srcStillImage.related_item = params[:srcStillImage][:related_item]
    srcStillImage.item_location = params[:srcStillImage][:item_location]
    srcStillImage.content_id = params[:srcStillImage][:content_id]
    srcStillImage.housing_id = params[:srcStillImage][:housing_id]
    srcStillImage.conservation_history = params[:srcStillImage][:conservation_history]
    srcStillImage.source_date = params[:srcStillImage][:source_date]
    srcStillImage.publication_date = params[:srcStillImage][:publication_date]
    
    srcStillImage.save
    
    render :partial => 'src_still_image_reload'
  end
  
#############################################################################
#AJAX Responders
#############################################################################
  def getNow
    if (params[:completed_by] != '0')
      render_text(Time::now)
    else
      render_text('&nbsp;')
    end
  end

  def updateMainEntry
    #return main_entry when Collection Number is changed
    
    dd = DescriptionData.find(params[:collection_number])    
    render_text(dd.main_entry)
  end
  def updateTitleStatement
    #return TitleStatement when Collection Number is changed
    
    dd = DescriptionData.find(params[:collection_number])    
    render_text(dd.title_statement)
  end    
end
