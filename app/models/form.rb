class Form < ActiveRecord::Base
  has_many :SrcStillImage

  def self.getForms(subform)
  
    case subform
      when "src_still_img"
        condition = "forms.form LIKE 'Still%' OR forms.form LIKE '%Arch%'"
    end
    
    @forms = find(:all, :select => 'form, id', :order => 'form', :conditions => condition)
    
    f = []    
    for form in @forms
      f << [form.form, form.id]
    end  
    
    return f
  end  
end
