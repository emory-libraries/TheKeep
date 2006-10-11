class Language < ActiveRecord::Base
  has_and_belongs_to_many :contents
  
  def self.getLanguages
    @languages = find(:all)
    
    lang = []    
    for l in @languages
      lang << [l.language, l.id]
    end  
    
    return lang
  end  
  
end
