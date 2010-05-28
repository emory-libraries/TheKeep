class Subject < ActiveRecord::Base
  belongs_to :Authority
  has_and_belongs_to_many :contents 
  
  
  def self.getSubjects
    @subjects = find(:all, :select => 'subject, id', :order => 'subject')
    
    sub = []    
    for subject in @subjects
      sub << [subject.subject, subject.id]
    end  
    
    return sub
  end  
end
